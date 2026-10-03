import pytest

from src.loaders import load_directory, load_document


def test_carga_txt_y_md(tmp_path):
    (tmp_path / "a.txt").write_text("contenido a", encoding="utf-8")
    (tmp_path / "b.md").write_text("# titulo", encoding="utf-8")
    sections = load_directory(tmp_path)
    assert {s.source for s in sections} == {"a.txt", "b.md"}


def test_ignora_formatos_no_soportados(tmp_path):
    (tmp_path / "foto.png").write_bytes(b"x")
    assert load_directory(tmp_path) == []


def test_formato_no_soportado_falla(tmp_path):
    archivo = tmp_path / "datos.csv"
    archivo.write_text("a,b", encoding="utf-8")
    with pytest.raises(ValueError):
        load_document(archivo)