from pathlib import Path
from typing import List
from pyconverters_grobid.grobid import GrobidConverter, GrobidParameters
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile


def test_grobid_xml():
    converter = GrobidConverter()
    parameters = GrobidParameters(sentences=True, citations=True)
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/PMC1636350.pdf')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'application/pdf'), parameters)
        assert len(docs) == 1
        assert docs[0].identifier
        assert docs[0].text
        assert docs[0].title
        assert 'TITLE' in docs[0].boundaries
        assert docs[0].annotations
        assert len(docs[0].annotations[0].terms) == 1
