import logging

from django.core.management import BaseCommand
from django.db import transaction
from tqdm import tqdm

from sitelfl.models.banners import Banners
from sitelfl.models.bottom_menu import Bottom_menu
from sitelfl.models.menu import Menu
from sitelfl.models.menu_items import MenuItems

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Восстановление данных"

    def handle(self, *args, **options):
        logger.info(self.help)

        old_url_template = 'lfl.ru'
        # new_url_template = 'debug.lfl.ru'
        new_url_template = 'lfl.dbg'

        with transaction.atomic():
            query = Menu.objects.using('sitelfl').filter()
            pbar = tqdm(total=query.count())

            for menu in query:
                old_link = menu.link
                link = menu.link
                link_items = link.split('/')
                recreated = False
                for link_item in link_items:
                    if link_item.find(new_url_template) == -1 and link_item.find(old_url_template) != -1:
                        link_items[link_items.index(link_item)] = link_item.replace(old_url_template, new_url_template)
                        recreated = True

                if recreated:
                    link = '/'.join(link_items)

                    # Recreated_urls.objects.using('sitelfl').update_or_create(old_urls=old_link, defaults=dict(new_urls=link, old_id=menu.id, table_name='menu'))
                    updated = Menu.objects.using('sitelfl').filter(link=old_link).update(link=link)
                    print(f'\n{link}')
                    print(f'Updated: {updated}')

                pbar.update()

            query = MenuItems.objects.using('sitelfl').filter()
            pbar = tqdm(total=query.count())
            for menu in query:
                old_link = menu.url
                link = menu.url
                link_items = link.split('/')
                recreated = False
                for link_item in link_items:
                    if link_item.find(new_url_template) == -1 and link_item.find(old_url_template) != -1:
                        link_items[link_items.index(link_item)] = link_item.replace(old_url_template, new_url_template)
                        recreated = True

                if recreated:
                    link = '/'.join(link_items)

                    # Recreated_urls.objects.using('sitelfl').update_or_create(old_urls=old_link, defaults=dict(new_urls=link, old_id=menu.id, table_name='menu_items'))
                    updated = MenuItems.objects.using('sitelfl').filter(url=old_link).update(url=link)
                    print(f'\n{link}')
                    print(f'Updated: {updated}')

                pbar.update()

            query = Bottom_menu.objects.using('sitelfl').filter()
            pbar = tqdm(total=query.count())
            for menu in query:
                old_link = menu.url
                link = menu.url
                link_items = link.split('/')
                recreated = False
                for link_item in link_items:
                    if link_item.find(new_url_template) == -1 and link_item.find(old_url_template) != -1:
                        link_items[link_items.index(link_item)] = link_item.replace(old_url_template, new_url_template)
                        recreated = True

                if recreated:
                    link = '/'.join(link_items)

                    try:
                        # Recreated_urls.objects.using('sitelfl').update_or_create(old_urls=old_link, defaults=dict(new_urls=link, old_id=menu.id, table_name='bottom_menu'))
                        updated = Bottom_menu.objects.using('sitelfl').filter(url=old_link).update(url=link)
                        print(f'\n{link}')
                        print(f'Updated: {updated}')
                    except Exception as ex:
                        print(f'\n{ex}')

                pbar.update()

            query = Banners.objects.using('sitelfl').filter()
            pbar = tqdm(total=query.count())
            for menu in query:
                old_link = menu.href
                link = menu.href
                link_items = link.split('/')
                recreated = False
                for link_item in link_items:
                    if link_item.find(new_url_template) == -1 and link_item.find(old_url_template) != -1:
                        link_items[link_items.index(link_item)] = link_item.replace(old_url_template, new_url_template)
                        recreated = True

                if recreated:
                    link = '/'.join(link_items)

                    try:
                        # Recreated_urls.objects.using('sitelfl').update_or_create(old_urls=old_link, defaults=dict(new_urls=link, old_id=menu.id, table_name='banners'))
                        updated = Banners.objects.using('sitelfl').filter(href=old_link).update(href=link)
                        print(f'\n{link}')
                        print(f'Updated: {updated}')
                    except Exception as ex:
                        print(f'\n{ex}')

                pbar.update()
