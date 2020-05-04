import download.download_scp
import generate.generate_epub

if __name__ == '__main__':
    generate.generate_epub.create_ebook(download.download_scp.get_scp_wiki())
