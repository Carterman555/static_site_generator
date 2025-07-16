import unittest
from functions import extract_markdown_images
from functions import extract_markdown_links


class TestExtractImagesAndLinks(unittest.TestCase):
    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        markdown_images = extract_markdown_images(text)

        target_markdown_images = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(markdown_images, target_markdown_images)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        markdown_links = extract_markdown_links(text)

        target_markdown_links = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(markdown_links, target_markdown_links)



    