import os
from collections import defaultdict
from functools import lru_cache
from typing import List, cast, Type

from grobid_client import Client
from grobid_client.api.pdf import process_fulltext_document
from grobid_client.models import ProcessForm, Article, TextWithRefs, Citation, ArticleCitations
from grobid_client.types import File, TEI
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, Sentence, Boundary, Annotation, Term
from starlette.datastructures import UploadFile

# _home = os.path.expanduser('~')
# xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or os.path.join(_home, '.cache')
APP_GROBID_URI = os.environ.get('APP_GROBID_URI', "https://cloud.science-miner.com/grobid")


class GrobidParameters(ConverterParameters):
    sourceText: bool = Field(False, description='Set source text in conversion output')
    sentences: bool = Field(False, description='Force sentence segmentation')
    figures: bool = Field(False, description='Do extract figures and tables descriptions')
    citations: bool = Field(False, description='Do extract bibliographic references in text')


class GrobidConverter(ConverterBase):
    """Grodbid PDF converter .
    """

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: GrobidParameters = \
            cast(GrobidParameters, parameters)

        client = get_client()
        doc = None
        form = ProcessForm(
            segment_sentences="1" if params.sentences else "0",
            input_=File(file_name=source.filename, payload=source.file, mime_type=source.content_type),
        )
        r = process_fulltext_document.sync_detailed(client=client, multipart_data=form)
        if r.is_success:
            doc = article_to_doc(r, params)
        else:
            r.raise_for_status()
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return GrobidParameters


def article_to_doc(response, params):
    article: Article = TEI.parse(response.content, figures=params.figures)
    doc = Document(identifier=article.identifier, title=article.title)
    if params.sourceText:
        doc.sourceText = response.content.decode("utf-8")
    doc.metadata = citation_to_metadata(article.bibliography)
    sections_to_text(doc, article.sections, article.citations, params)
    return doc


def citation_to_metadata(citation: Citation):
    metadata = {}
    if citation.main_title:
        metadata['main_title'] = str(citation.main_title)
    if citation.published:
        metadata['published'] = str(citation.published)
    if citation.publisher:
        metadata['publisher'] = citation.publisher
    if citation.ids:
        for k, v in citation.ids.additional_properties.items():
            metadata[k] = v
    if citation.authors:
        authors, affiliations = authors_and_affiliations(citation.authors)
        metadata['authors'] = authors
        metadata['affiliations'] = affiliations
    if citation.titles:
        for k, v in citation.titles.additional_properties.items():
            metadata['title_' + k] = v
    if citation.scopes:
        for k, v in citation.scopes.additional_properties.items():
            metadata[k] = v
    return metadata


def authors_and_affiliations(author_list):
    authors = set()
    affiliations = set()
    if author_list:
        for author in author_list:
            auth = []
            if author.pers_name.firstname:
                auth.append(author.pers_name.firstname)
            if author.pers_name.middlename:
                auth.append(author.pers_name.middlename)
            if author.pers_name.surname:
                auth.append(author.pers_name.surname)
            authors.add(" ".join(auth))
            if author.affiliations:
                for affiliation in author.affiliations:
                    aff = []
                    if affiliation.institution:
                        aff.append(affiliation.institution)
                    if affiliation.department:
                        aff.append(affiliation.department)
                    if affiliation.laboratory:
                        aff.append(affiliation.laboratory)
                    affiliations.add(", ".join(aff))
    return list(authors), list(affiliations)


def sections_to_text(doc, sections, citations: ArticleCitations, params):
    ref2citations = {}
    if params.citations and citations:
        for ref, citation in citations.additional_properties.items():
            ref2citations['#' + ref] = citation_to_metadata(citation)
    if sections:
        text_buf = []
        sentences = []
        annotations = []
        boundaries = defaultdict(list)
        for section in sections:
            start = sum(map(len, text_buf))
            bstart = start
            text_buf.append((section.name if section.name is not None else "") + "\n")
            end = sum(map(len, text_buf))
            sentences.append(Sentence(start=start, end=end))
            if section.paragraphs:
                for paragraph in section.paragraphs:
                    if params.sentences:
                        for i, sentence in enumerate(paragraph):
                            sent, annots = add_references(sentence, text_buf, ref2citations)
                            sentences.append(sent)
                            if params.citations:
                                annotations.extend(annots)
                            if i < len(paragraph) - 1:
                                text_buf.append(" ")
                        text_buf.append("\n")
                    else:
                        sent, annots = add_references(paragraph, text_buf, ref2citations)
                        sentences.append(sent)
                        if params.citations:
                            annotations.extend(annots)
                        text_buf.append("\n")
            text_buf.append("\n")
            bend = sum(map(len, text_buf))
            boundaries[section.name].append(Boundary(start=bstart, end=bend))
        doc.text = "".join(text_buf)
        if params.citations:
            doc.annotations = annotations
        doc.sentences = sentences
        doc.boundaries = boundaries


def add_references(sentence: TextWithRefs, text_buf: List[str], ref2citations):
    annotations = []
    start = sum(map(len, text_buf))
    text_buf.append(sentence.text + " ")
    end = sum(map(len, text_buf))
    if sentence.refs:
        for ref in sentence.refs:
            if ref.type == "bibr":
                a = Annotation(label="Citation", labelName="citation",
                               text=sentence.text[ref.start:ref.end],
                               start=start + ref.start, end=start + ref.end)
                props = ref2citations.get(ref.target, None)
                if props:
                    term_id = props.pop('main_title', 'Unknown')
                    a.terms = [Term(identifier=term_id, lexicon="grobid", properties=props)]
                annotations.append(a)
    return Sentence(start=start, end=end), annotations


@lru_cache(maxsize=None)
def get_client():
    return Client(base_url=APP_GROBID_URI + "/api", timeout=600)
