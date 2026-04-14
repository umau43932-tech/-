from pathlib import Path
import tempfile
import unittest

from file_organizer import get_category, organize_directory


class FileOrganizerTests(unittest.TestCase):
    def test_get_category(self):
        self.assertEqual(get_category(Path("a.jpg")), "Images")
        self.assertEqual(get_category(Path("b.pdf")), "Documents")
        self.assertEqual(get_category(Path("c.unknown")), "Others")

    def test_organize_directory_moves_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "photo.jpg"
            doc = root / "memo.txt"
            image.write_text("img")
            doc.write_text("doc")

            results = organize_directory(root, move_files=True)

            self.assertEqual(len(results), 2)
            self.assertTrue((root / "Images" / "photo.jpg").exists())
            self.assertTrue((root / "Documents" / "memo.txt").exists())
            self.assertFalse(image.exists())

    def test_organize_directory_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code = root / "main.py"
            code.write_text("print('hi')")

            results = organize_directory(root, move_files=False)

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].destination, root / "Code" / "main.py")
            self.assertTrue(code.exists())


if __name__ == "__main__":
    unittest.main()
