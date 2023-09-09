from post_inamtes_daily import make_post
from delete_posts import remove_posts
from scraper_2 import URLScraper, InmatesScraper
from util.files_reader import read_post_id_json, save_post_ids, xpath_reader


def run_scraper():
    """
    Scraping daily updated inmates
    :return:
    """
    print('Running daily scraper')
    my_scraper = URLScraper()
    my_scraper.scrap_inmates_url()
    inmates_scraper = InmatesScraper()
    inmates_scraper.scrap_inmates_data()


def run_posting():
    try:
        print('Removing posts...')
        for items in read_post_id_json():
            remove_posts(post_id=items['id'])
        jail_names = xpath_reader()
        print('Posting new data...')
        for items in jail_names:
            make_post(items['jail_name'])
    except Exception:
        jail_names = xpath_reader()
        print('Posting new data...')
        for items in jail_names:
            make_post(items['jail_name'])


if __name__ == '__main__':
    # run_scraper()
    run_posting()
