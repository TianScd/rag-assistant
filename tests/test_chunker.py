import pytest

from src.chunker import chunk_sections, chunk_text
from src.loaders import Section


def test_rechaza_overlap_invalido():
    with pytest.raises(ValueError):
        chunk_text("hola", chunk_size=100, overlap=100)


def test_texto_corto_da_un_solo_fragmento():
    assert chunk_text("Texto corto.", 800, 100) == ["Texto corto."]


def test_ningun_fragmento_supera_el_limite():
    text = " ".join(f"palabra{i}" for i in range(500))
    assert all(len(c) <= 200 for c in chunk_text(text, 200, 40))


def test_no_se_pierden_palabras():
    words = [f"palabra{i}" for i in range(500)]
    chunks = chunk_text(" ".join(words), 200, 40)
    assert set(words) <= set(" ".join(chunks).split())


def test_termina_con_texto_sin_espacios():
    chunks = chunk_text("a" * 5000, 200, 40)
    assert chunks and all(len(c) <= 200 for c in chunks)


def test_conserva_metadata_e_indices():
    sections = [Section(text="uno dos tres " * 100, source="a.txt", page=None)]
    chunks = chunk_sections(sections, 200, 40)
    assert [c.index for c in chunks] == list(range(len(chunks)))
    assert all(c.source == "a.txt" for c in chunks)