import logging
from datetime import date

from django.conf import settings
from django.db import connections, transaction
from django.utils import timezone
from tqdm import tqdm

from isc_common.auth.models.user import User
from isc_common.auth.models.user_e_mails import User_e_mails
from isc_common.auth.models.user_phones import User_phones
from isc_common.auth.models.usergroup import UserGroup
from isc_common.common import unknown
from isc_common.datetime import StrToDate, DateTimeToStr
from isc_common.managers.common_manager import lazy_bulk_fetch
from isc_common.models.audit import AuditModel
from isc_common.models.standard_colors import Standard_colors
from isc_common.models.users_images import Users_images
from isc_common.number import StrToNumber, IntToBool
from lfl_admin.common.models.posts import Posts
from lfl_admin.competitions.management.commands.restruct_divisions import restruct_divisions
from lfl_admin.competitions.models.assists import Assists
from lfl_admin.competitions.models.calendar import Calendar
from lfl_admin.competitions.models.calendar_images import Calendar_images
from lfl_admin.competitions.models.calendar_links import Calendar_links
from lfl_admin.competitions.models.calendar_text_informations import Calendar_text_informations
from lfl_admin.competitions.models.card_types import Card_types
from lfl_admin.competitions.models.cards import Cards
from lfl_admin.competitions.models.club_admins import Club_admins
from lfl_admin.competitions.models.club_contacts import Club_contacts
from lfl_admin.competitions.models.club_histories import Club_histories
from lfl_admin.competitions.models.clubs import Clubs
from lfl_admin.competitions.models.clubs_images import Clubs_images
from lfl_admin.competitions.models.clubs_links import Clubs_links
from lfl_admin.competitions.models.disqualification_condition import Disqualification_condition
from lfl_admin.competitions.models.disqualification_types import Disqualification_types
from lfl_admin.competitions.models.disqualification_zones import Disqualification_zones
from lfl_admin.competitions.models.disqualifications import Disqualifications
from lfl_admin.competitions.models.divisions import Divisions
from lfl_admin.competitions.models.divisions_images import Divisions_images
from lfl_admin.competitions.models.fines import Fines
from lfl_admin.competitions.models.fines_text_informations import Fines_text_informations
from lfl_admin.competitions.models.formation import Formation
from lfl_admin.competitions.models.fouls import Fouls
from lfl_admin.competitions.models.goals import Goals
from lfl_admin.competitions.models.goals_type import Goals_type
from lfl_admin.competitions.models.keepers import Keepers
from lfl_admin.competitions.models.leagues import Leagues
from lfl_admin.competitions.models.leagues_images import Leagues_images
from lfl_admin.competitions.models.leagues_links import Leagues_links
from lfl_admin.competitions.models.leagues_text_informations import Leagues_text_informations
from lfl_admin.competitions.models.match_stat_types import Match_stat_types
from lfl_admin.competitions.models.match_stats import Match_stats
from lfl_admin.competitions.models.matchdays import Matchdays
from lfl_admin.competitions.models.penalties import Penalties
from lfl_admin.competitions.models.player_histories import Player_histories
from lfl_admin.competitions.models.player_old_ids import Player_old_ids
from lfl_admin.competitions.models.players import Players
from lfl_admin.competitions.models.players_change_history import Players_change_history
from lfl_admin.competitions.models.players_change_history_text_informations import Players_change_history_text_informations
from lfl_admin.competitions.models.players_images import Players_images
from lfl_admin.competitions.models.players_text_information import Players_text_informations
from lfl_admin.competitions.models.protocol_types import Protocol_types
from lfl_admin.competitions.models.referee_category import Referee_category
from lfl_admin.competitions.models.referee_zone import Referee_zone
from lfl_admin.competitions.models.referees import Referees
from lfl_admin.competitions.models.referees_images import Referees_images
from lfl_admin.competitions.models.seasons import Seasons
from lfl_admin.competitions.models.squads import Squads
from lfl_admin.competitions.models.squads_match import Squads_match
from lfl_admin.competitions.models.squads_text_informations import Squads_text_informations
from lfl_admin.competitions.models.statistics_types import Statistics_types
from lfl_admin.competitions.models.tournament_member_doubles import Tournament_member_doubles
from lfl_admin.competitions.models.tournament_members import Tournament_members
from lfl_admin.competitions.models.tournament_types import Tournament_types
from lfl_admin.competitions.models.tournaments import Tournaments
from lfl_admin.competitions.models.tournaments_images import Tournaments_images
from lfl_admin.constructions.models.fields import Fields
from lfl_admin.constructions.models.fields_images import Fields_images
from lfl_admin.constructions.models.stadium_rating import Stadium_rating
from lfl_admin.constructions.models.stadium_zones import Stadium_zones
from lfl_admin.constructions.models.stadiums import Stadiums
from lfl_admin.constructions.models.stadiums_images import Stadiums_images
from lfl_admin.constructions.models.stadiums_text_informations import Stadiums_text_informations
from lfl_admin.decor.models.banners import Banners
from lfl_admin.decor.models.banners_type import Banners_type
from lfl_admin.decor.models.bottom_menu import Bottom_menu
from lfl_admin.decor.models.menu import Menu
from lfl_admin.decor.models.menu_item_leagues import Menu_item_leagues
from lfl_admin.decor.models.menu_items import Menu_items
from lfl_admin.decor.models.menu_items_images import Menu_items_images
from lfl_admin.decor.models.menu_items_links import Menu_items_links
from lfl_admin.decor.models.menu_type import Menu_type
from lfl_admin.decor.models.menu_zone_types import Menu_zone_types
from lfl_admin.decor.models.menu_zones import Menu_zones
from lfl_admin.decor.models.menus_images import Menus_images
from lfl_admin.decor.models.menus_links import Menus_links
from lfl_admin.decor.models.news import News
from lfl_admin.decor.models.news_action_types import News_action_types
from lfl_admin.decor.models.news_actions import News_actions
from lfl_admin.decor.models.news_favorites import News_favorites
from lfl_admin.decor.models.news_icon_type import News_icon_type
from lfl_admin.decor.models.news_images import News_images
from lfl_admin.decor.models.news_links import News_links
from lfl_admin.decor.models.news_quantity_by_url import NewsQuantity_ByUrl
from lfl_admin.decor.models.news_start_block_tournament import News_start_block_tournament
from lfl_admin.decor.models.news_start_block_tournament_text_informations import News_start_block_tournament_text_informations
from lfl_admin.decor.models.news_text_informations import News_text_informations
from lfl_admin.decor.models.news_type import News_type
from lfl_admin.inventory.models.clothes import Clothes
from lfl_admin.inventory.models.clothes_clubs import Clothes_clubs
from lfl_admin.inventory.models.clothes_images import Clothes_images
from lfl_admin.inventory.models.clothes_type import Clothes_type
from lfl_admin.region.models.cities import Cities
from lfl_admin.region.models.city_images import City_images
from lfl_admin.region.models.interregion import Interregion
from lfl_admin.region.models.region_images import Region_images
from lfl_admin.region.models.region_links import Region_links
from lfl_admin.region.models.region_text_information import Region_text_informations
from lfl_admin.region.models.region_zones import Region_zones
from lfl_admin.region.models.regions import Regions
from lfl_admin.user_ext.models.administrators import Administrators
from lfl_admin.user_ext.models.contacts import Contacts
from lfl_admin.user_ext.models.contacts_e_mails import Contacts_e_mails
from lfl_admin.user_ext.models.contacts_phones import Contacts_phones
from lfl_admin.user_ext.models.person_club_photos import Person_club_photos
from lfl_admin.user_ext.models.persons import Persons
from lfl_admin.user_ext.models.users_regions import Users_regions
from sitelfl.models.administrators import Administrators as OldAdministrators
from sitelfl.models.assists import Assists as OldAssists
from sitelfl.models.banners import Banners as OldBanners
from sitelfl.models.bottom_menu import Bottom_menu as OldBottom_menu
from sitelfl.models.calendar import Calendar as OldCalendar
from sitelfl.models.cards import Cards as OldCards
from sitelfl.models.cities import Cities as OldCities
from sitelfl.models.club_admins import ClubAdmins
from sitelfl.models.club_contacts import ClubContacts
from sitelfl.models.club_histories import ClubHistories
from sitelfl.models.clubs import Clubs as OldClubs
from sitelfl.models.contacts import Contacts as OldContacts
from sitelfl.models.discvalification_zones import DisqualificationZones
from sitelfl.models.disqualifications import Disqualifications as OldDisqualifications
from sitelfl.models.divisions import Divisions as OldDivisions
from sitelfl.models.fields import Fields as OldFields
from sitelfl.models.fines import Fines as OldFines
from sitelfl.models.formation import Formation as OldFormation
from sitelfl.models.fouls import Fouls as OldFouls
from sitelfl.models.goals import Goals as OldGoals
from sitelfl.models.images import Images as OldImages
from sitelfl.models.keepers import Keepers as OldKeepers
from sitelfl.models.leagues import Leagues as OldLeagues
from sitelfl.models.match_stats import MatchStats
from sitelfl.models.matchdays import Matchdays as OldMatchdays
from sitelfl.models.menu import Menu as OldMenu
from sitelfl.models.menu_item_leagues import MenuItemLeagues
from sitelfl.models.menu_items import MenuItems
from sitelfl.models.menu_zones import MenuZones
from sitelfl.models.news import News as OldNews
from sitelfl.models.news_actions import NewsActions
from sitelfl.models.news_favorites import NewsFavorites
from sitelfl.models.news_quantity_by_url import NewsQuantityByUrl
from sitelfl.models.news_start_block_tournament import NewsStartBlockTournament
from sitelfl.models.penalties import Penalties as OldPenalties
from sitelfl.models.person_club_photos import PersonClubPhotos
from sitelfl.models.person_photos import PersonPhotos
from sitelfl.models.persons import Persons as OldPersons
from sitelfl.models.player_histories import PlayerHistories
from sitelfl.models.players import Players as OldPlayers
from sitelfl.models.players_change_history import PlayersChangeHistory
from sitelfl.models.referee_category import RefereeCategory
from sitelfl.models.referee_zone import RefereeZone
from sitelfl.models.referees import Referees as OldReferees
from sitelfl.models.regions import Regions as OldRegions
from sitelfl.models.seasons import Seasons as OldSeasons
from sitelfl.models.shirt_images import ShirtImages
from sitelfl.models.shirts import Shirts
from sitelfl.models.squads import Squads as OldSquads
from sitelfl.models.squads_match import SquadsMatch
from sitelfl.models.stadium_rating import StadiumRating
from sitelfl.models.stadium_zones import StadiumZones
from sitelfl.models.stadiums import Stadiums as OldStadiums
from sitelfl.models.tournament_member_doubles import TournamentMemberDoubles
from sitelfl.models.tournament_members import TournamentMembers
from sitelfl.models.tournaments import Tournaments as OldTournaments

logger = logging.getLogger(__name__)


def get_ids_from_old_ids(model):
    s = set()
    for item in model.objects.exclude(old_ids = None):
        s.update(set(item.old_ids))
    return list(s)


def migrate_base(mode):
    modes = mode.split(' ')
    if mode == 'all':
        modes = [
            'administrators',
            'assists',
            'banners',
            'bottom_menu',
            'calendar',
            'cards',
            'cities',
            'club_admins',
            'club_contacts',
            'club_histories',
            'clubs',
            'contacts',
            'disqualification_zones',
            'disqualifications',
            'divisions',
            'fields',
            'fines',
            'formation',
            'fouls',
            'goals',
            'keepers',
            'leagues',
            'match_stats',
            'matchdays',
            'menu',
            'menu_item',
            'menu_item_league',
            'menu_zones',
            'news',
            'news_actions',
            'news_favorites',
            'news_quantity_by_url',
            'news_start_block_tournament',
            'penalties'
            'person_club_photos',
            'person_photos',
            'persons',
            'player_histories',
            'players',
            'players_change_history',
            'referee_category',
            'referee_zone',
            'referees',
            'region',
            'region_zones',
            'seasons',
            'shirts',
            'shirts_images',
            'squads',
            'squads_match',
            'stadium_rating',
            'stadium_zones',
            'stadiums',
            'tournament_member_doubles',
            'tournament_members',
            'tournaments',
        ]

    o_ssh_client = settings.SSH_CLIENTS.client(settings.OLD_FILES)

    def sync_administrators():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ administrators ===============================')

        for administrator in OldAdministrators.objects.using('sitelfl').values('admin_post').distinct():
            administrator = administrator.get('admin_post')
            administrator_code = AuditModel.translit(administrator)

            post, created = Posts.objects.update_or_create(
                code = administrator_code,
                defaults = dict(
                    name = administrator,
                    editing = False,
                    deliting = False,
                ))

        OldAdministratorsQuery = OldAdministrators.objects.using('sitelfl').exclude(admin_id__in = map(lambda x: x.old_id, Administrators.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = OldAdministratorsQuery.count())

        for administrator in OldAdministratorsQuery:
            with transaction.atomic():
                if administrator.active == 1:
                    props = Administrators.props.active

                if administrator.send_email == 1:
                    props |= Administrators.props.send_email

                if administrator.kdk_fine_deleting == 1:
                    props |= Administrators.props.kdk_fine_deleting

                if administrator.person_editing == 1:
                    props |= Administrators.props.person_editing

                if administrator.all_news_access == 1:
                    props |= Administrators.props.all_news_access

                if administrator.public_access == 1:
                    props |= Administrators.props.public_access

                if administrator.transfer_right == 1:
                    props |= Administrators.props.transfer_right

                for access in administrator.access.split(','):
                    if access == '':
                        pbar.update()
                        continue

                    if access == 'news':
                        props |= Administrators.props.news
                    elif access == 'documents':
                        props |= Administrators.props.documents
                    elif access == 'official':
                        props |= Administrators.props.official
                    elif access == 'documents':
                        props |= Administrators.props.documents
                    elif access == 'video':
                        props |= Administrators.props.video
                    elif access == 'blocks':
                        props |= Administrators.props.blocks
                    elif access == 'upload':
                        props |= Administrators.props.upload
                    elif access == 'tournament_members':
                        props |= Administrators.props.tournament_members
                    else:
                        raise Exception(f'tag: {access} unregistered')

                names = administrator.name.split(' ')
                last_name = first_name = middle_name = None
                if len(names) == 3:
                    last_name, first_name, middle_name = names

                if len(names) == 2:
                    last_name, first_name = names

                if len(names) == 1:
                    last_name, = names

                user, created = User.objects.get_or_create(  # !!! get_or_create не менять
                    username = administrator.login,
                    defaults = dict(
                        description = administrator.clubs,
                        first_name = first_name,
                        last_name = last_name,
                        lastmodified = administrator.last_edit_date,
                        middle_name = middle_name,
                    ))

                group, created = UserGroup.objects.update_or_create(code = AuditModel.translit(administrator.admin_post), name = administrator.admin_post)
                try:
                    user.usergroup.add(group)
                except:
                    pass
                Administrators.objects.update_or_create(
                    old_id = administrator.admin_id,
                    defaults = dict(
                        user = user,
                        register_date = administrator.register_date,
                    ))

                Users_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = administrator.photo, main_model = user, keyimage = 'photo', path = 'admin')
            pbar.update()

        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End administrators ==========================')

    def sync_region_zones():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ region_zones ===============================')
        oldRegionQuery = OldRegions.objects.values('region_zone_id').using('sitelfl').exclude(region_zone_id__in = map(lambda x: x.old_id, Region_zones.objects.filter(old_id__isnull = False))).distinct()
        pbar = tqdm(total = oldRegionQuery.count())

        for oldRegion in oldRegionQuery:
            region_zone_id = oldRegion.get('region_zone_id')
            region_zones, created = Region_zones.objects.update_or_create(
                old_id = region_zone_id,
                defaults = dict(
                    code = region_zone_id,
                    name = region_zone_id,
                    editing = False,
                    deliting = False,
                ))
            pbar.update()

        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End region_zones ==========================')

    def sync_seasons():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ seasons ===============================')
        oldSessionQuery = OldSeasons.objects.using('sitelfl').exclude(season_id__in = map(lambda x: x.old_id, Seasons.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = oldSessionQuery.count())
        for oldSeason in oldSessionQuery.all():
            props = 0
            if oldSeason.active == 1:
                props |= Seasons.props.active

            season, created = Seasons.objects.update_or_create(
                old_id = oldSeason.season_id,
                defaults = dict(
                    code = AuditModel.translit(oldSeason.name),
                    deliting = False,
                    description = oldSeason.comment,
                    editing = False,
                    end_date = oldSeason.end_date,
                    name = oldSeason.name,
                    props = props,
                    start_date = oldSeason.start_date,
                ))
            if created is True:
                logger.debug(season)
            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End seasons ==========================')

    def sync_cities():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ cities ===============================')
        OldCitiesQuery = OldCities.objects.using('sitelfl').exclude(city_id__in = map(lambda x: x.old_id, Cities.objects.filter(old_id__isnull = False)))

        pbar = tqdm(total = OldCitiesQuery.count())
        for oldCities in OldCitiesQuery:
            if oldCities.name == '':
                pbar.update()
                continue

            city, _ = Cities.objects.update_or_create(
                old_id = oldCities.city_id,
                defaults = dict(
                    name = oldCities.name
                )
            )

            City_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldCities.logo, main_model = city, keyimage = 'logo', path = 'cities', exception = True)
            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ End cities ===============================')

    def sync_region():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ region ===============================')
        oldRegionsQuery = OldRegions.objects.using('sitelfl').exclude(region_id__in = map(lambda x: x.old_id, Regions.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = oldRegionsQuery.count())
        for oldRegion in oldRegionsQuery:
            with transaction.atomic():
                props = 0
                if oldRegion.active == 1:
                    props |= Regions.props.active

                if oldRegion.select_division == 1:
                    props |= Regions.props.select_division

                if oldRegion.parimatch == 1:
                    props |= Regions.props.parimatch

                if oldRegion.select_division == 1:
                    props |= Regions.props.select_division

                if oldRegion.leagues_menu == 1:
                    props |= Regions.props.leagues_menu

                if oldRegion.submenu == 1:
                    props |= Regions.props.submenu

                color, _ = Standard_colors.objects.update_or_create(code = AuditModel.translit(oldRegion.color), defaults = dict(name = oldRegion.color))

                region, created = Regions.objects.update_or_create(
                    old_id = oldRegion.region_id,
                    defaults = dict(
                        color = color,
                        description = oldRegion.text,
                        editor = Administrators.objects.get_user(oldRegion.edited_by_id),
                        name = oldRegion.name,
                        priority = oldRegion.priority,
                        props = props,
                        season = Seasons.objects.getOr(old_id = oldRegion.current_season_id, alternative = Seasons.unknown),
                        zone = Region_zones.objects.getOr(old_id = oldRegion.region_zone_id, alternative = Region_zones.unknown),
                    ))

                Region_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldRegion.logo, main_model = region, keyimage = 'logo', path = 'regions', exception = False)
                Region_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldRegion.double_logo, main_model = region, keyimage = 'double_logo', path = 'regions', exception = False)
                Region_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldRegion.right_logo, main_model = region, keyimage = 'right_logo', path = 'regions', exception = False)
                Region_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldRegion.header, main_model = region, keyimage = 'header', path = 'regions', exception = False)

                Region_text_informations.objects.update_or_create(region = region, code = 'contacts', defaults = dict(text = oldRegion.contacts))
                Region_text_informations.objects.update_or_create(region = region, code = 'middle_text', defaults = dict(text = oldRegion.middle_text))

                Region_links.objects.update_or_create(region = region, code = 'right_link', defaults = dict(link = oldRegion.right_link))
                Region_links.objects.update_or_create(region = region, code = 'middle_link', defaults = dict(link = oldRegion.middle_link))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End region ==========================')

    def sync_banners():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ banners ===============================')
        query = OldBanners.objects.all().using('sitelfl').exclude(id__in = map(lambda x: x.old_id, Banners.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())
        for oldBanner in query:
            with transaction.atomic():
                banners_type, created = Banners_type.objects.update_or_create(code = oldBanner.banner_type, name = oldBanner.banner_type)

                props = 0
                if oldBanner.active == 1:
                    props |= Banners.props.active

                banner, created = Banners.objects.update_or_create(
                    old_id = oldBanner.id,
                    defaults = dict(
                        banner_type = banners_type,
                        props = props,
                        padding_top = oldBanner.padding_top,
                        position = oldBanner.position,
                        rotate = oldBanner.rotate,
                        region = Regions.objects.getOptional(old_id = oldBanner.region_id)
                    ))

                Banners.update_or_create_link(main_model = banner, link_field_name = 'href', link = oldBanner.href)
                Banners.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldBanner.image, main_model = banner, keyimage = 'image', path = 'banners', self_image_field = True, image_field_name = 'image')

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End banners ==========================')

    def sync_leagues():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ leagues ===============================')
        oldLeaguesQuery = OldLeagues.objects.using('sitelfl').exclude(league_id__in = map(lambda x: x.old_id, Leagues.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = oldLeaguesQuery.count())
        for oldLeague in oldLeaguesQuery:
            props = 0
            if oldLeague.active == 1:
                props |= Leagues.props.active

            if oldLeague.parimatch == 1:
                props |= Leagues.props.parimatch

            if oldLeague.show_in_menu == 1:
                props |= Leagues.props.show_in_menu

            if oldLeague.show_referee_photo_in_protocols == 1:
                props |= Leagues.props.show_referee_photo_in_protocols

            if oldLeague.show_stadium_photo_in_protocols == 1:
                props |= Leagues.props.show_stadium_photo_in_protocols

            if oldLeague.show_shirt_in_protocols == 1:
                props |= Leagues.props.show_shirt_in_protocols

            if oldLeague.submenu == 1:
                props |= Leagues.props.submenu

            if oldLeague.nonphoto == 1:
                props |= Leagues.props.nonphoto

            with transaction.atomic():
                league, created = Leagues.objects.update_or_create(
                    old_id = oldLeague.league_id,
                    defaults = dict(
                        add_slideshow_tabs = oldLeague.add_slideshow_tabs,
                        code = oldLeague.short_name,
                        description = oldLeague.text,
                        editor = Administrators.objects.get_user(oldLeague.edited_by_id),
                        name = oldLeague.name,
                        position = oldLeague.position,
                        referees_max = oldLeague.referees_max,
                        region = Regions.objects.getOr(old_id = oldLeague.region_id, alternative = Regions.unknown),
                        season = Seasons.objects.get(old_id = oldLeague.season_id),
                        slideshow_title = oldLeague.slideshow_title,
                    ))

                Leagues_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldLeague.logo, main_model = league, keyimage = 'logo', exception = False, path = 'leagues')
                Leagues_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldLeague.double_logo, main_model = league, keyimage = 'double_logo', exception = False, path = 'leagues')
                Leagues_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldLeague.right_logo, main_model = league, keyimage = 'right_logo', exception = False, path = 'leagues')
                Leagues_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldLeague.header, main_model = league, keyimage = 'header', exception = False, path = 'leagues')

                Leagues_text_informations.objects.update_or_create(league = league, code = 'contacts', defaults = dict(text = oldLeague.contacts))
                Leagues_text_informations.objects.update_or_create(league = league, code = 'social', defaults = dict(text = oldLeague.social))
                Leagues_text_informations.objects.update_or_create(league = league, code = 'middle_text', defaults = dict(text = oldLeague.middle_text))

                Leagues_links.objects.update_or_create(league = league, code = 'right_link', defaults = dict(link = oldLeague.right_link))
                Leagues_links.objects.update_or_create(league = league, code = 'middle_link', defaults = dict(link = oldLeague.middle_link))
                Leagues_links.objects.update_or_create(league = league, code = 'bg_link', defaults = dict(link = oldLeague.bg_link))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End leagues ==========================')

    def sync_stadium_rating():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ stadium_rating ===============================')
        oldStadiumRatingQuery = StadiumRating.objects.using('sitelfl').exclude(stadium_id__in = map(lambda x: x.old_id, Stadium_rating.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = oldStadiumRatingQuery.count())
        for oldOldStadium in oldStadiumRatingQuery:
            Stadium_rating.objects.update_or_create(
                old_id = oldOldStadium.stadium_id,
                defaults = dict(
                    stadium = Stadiums.objects.get(old_ids__overlap = [oldOldStadium.stadium_id]),
                    league = Leagues.objects.get(old_id = oldOldStadium.league_id),
                    rating = oldOldStadium.rating
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End stadium_rating ==========================')

    def sync_bottom_menu():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ bottom_menu ===============================')
        bottom_menuQuery = OldBottom_menu.objects.using('sitelfl').exclude(id__in = map(lambda x: x.old_id, Bottom_menu.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = bottom_menuQuery.count())

        for bottom_menu in bottom_menuQuery:
            with transaction.atomic():
                menu, _ = Bottom_menu.objects.update_or_create(
                    old_id = bottom_menu.id,
                    menu_type = Menu_type.objects.update_or_create(code = f'bottom_menu_{bottom_menu.type}', defaults = dict(name = f'bottom_menu_{bottom_menu.type}'))[0],
                    defaults = dict(
                        position = bottom_menu.position,
                        name = bottom_menu.name,
                    )
                )

                Menus_links.objects.update_or_create(menu = menu, code = 'bottom_menu_link', defaults = dict(link = bottom_menu.url))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End bottom_menu ==========================')

    def sync_menu():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ menu ===============================')
        query = OldMenu.objects.using('sitelfl').exclude(id__in = map(lambda x: x.old_id, Menu.objects.filter(old_id__isnull = False))).order_by('parent_id')
        pbar = tqdm(total = query.count())

        for menu in query:
            with transaction.atomic():
                props = 0
                if menu.active == 1:
                    props |= Menu.props.active

                if menu.blank == 1:
                    props = Menu.props.blank

                if menu.columns == 1:
                    props = Menu.props.columns

                _menu, _ = Menu.objects.update_or_create(
                    old_id = menu.id,
                    menu_type = Menu_type.objects.update_or_create(code = f'menu_{menu.type}', defaults = dict(name = f'menu_{menu.type}'))[0],
                    defaults = dict(
                        cookies = menu.cookies,
                        editor = Administrators.objects.get_user(menu.edited_by_id),
                        league = Leagues.objects.getOr(old_id = menu.league_id, alternative = Leagues.unknown),
                        level = menu.level,
                        name = menu.name,
                        parent = Menu.objects.getOptional(old_id = menu.parent_id),
                        position = menu.position,
                        props = props,
                        region = Regions.objects.getOr(old_id = menu.region_id, alternative = Regions.unknown),
                        style = menu.style,
                        subname = menu.subname,
                    )
                )

                Menus_links.objects.update_or_create(menu = _menu, code = 'menu_link', defaults = dict(link = menu.link))
                Menus_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = menu.image, main_model = _menu, keyimage = 'image', path = 'menu', exception = True)

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End menu ==========================')

    def sync_menu_items():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ menu_item ===============================')
        query = MenuItems.objects.using('sitelfl').exclude(id__in = map(lambda x: x.old_id, Menu_items.objects.filter(old_id__isnull = False))).order_by('parent_id')
        pbar = tqdm(total = query.count())

        for menu_item in query:
            with transaction.atomic():
                props = 0
                if menu_item.active == 1:
                    props |= Menu_items.props.active

                if menu_item.target == 1:
                    props |= Menu_items.props.target

                _menu_item, _ = Menu_items.objects.update_or_create(
                    old_id = menu_item.id,
                    menu_type = Menu_type.objects.update_or_create(code = 'menu_item', defaults = dict(name = f'menu_item'))[0],
                    defaults = dict(
                        name = menu_item.name,
                        parent = Menu_items.objects.getOptional(old_id = menu_item.parent_id),
                        position = menu_item.position,
                        props = props,
                    )
                )

                Menu_items_links.objects.update_or_create(menu_item = _menu_item, code = 'menu_item_link', defaults = dict(link = menu_item.url))
                Menu_items_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = menu_item.img, main_model = _menu_item, keyimage = 'img', path = 'menu_image', exception = False)

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End menu_item ==========================')

    def sync_menu_items_leagues():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ menu_item_league ===============================')
        query = MenuItemLeagues.objects.using('sitelfl').exclude(id__in = map(lambda x: x.old_id, Menu_item_leagues.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())

        for menu_item in query:
            with transaction.atomic():
                Menu_item_leagues.objects.update_or_create(
                    old_id = menu_item.id,
                    defaults = dict(
                        league = Leagues.objects.getOr(old_id = menu_item.league_id, alternative = Leagues.unknown),
                        region = Regions.objects.getOr(old_id = menu_item.region_id, alternative = Regions.unknown),
                        menu_item = Menu_items.objects.getOr(old_id = menu_item.menu_item.id, alternative = Menu_items.unknown),
                    )
                )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End menu_item_league ==========================')

    def sync_disqualification_zones():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ disqualification_zones ===============================')
        DisqualificationZonesQuery = DisqualificationZones.objects.using('sitelfl').exclude(zone_id__in = get_ids_from_old_ids(model = Disqualification_zones))
        pbar = tqdm(total = DisqualificationZonesQuery.count())

        for DisqualificationZone in DisqualificationZonesQuery:
            props = 0
            with transaction.atomic():
                if DisqualificationZone.active == 1:
                    props |= Disqualification_zones.props.active

                region = Regions.objects.getOr(old_id = DisqualificationZone.region_id, alternative = Regions.unknown)
                disqualification_zone = Disqualification_zones.objects.getOptional(code = f'{DisqualificationZone.name}_{region.id}', )

                if disqualification_zone is None:
                    disqualification_zone, created = Disqualification_zones.objects.update_or_create(
                        old_ids__overlap = [DisqualificationZone.zone_id],
                        defaults = dict(
                            editor = Administrators.objects.get_user(DisqualificationZone.edited_by_id),
                            code = f'{DisqualificationZone.name}_{region.id}',
                            name = DisqualificationZone.name,
                            number_of_yellowsold = DisqualificationZone.number_of_yellowsold,
                            props = props,
                            region = region,
                        )
                    )
                else:
                    created = False

                if created is False:
                    if DisqualificationZone.zone_id not in disqualification_zone.old_ids:
                        disqualification_zone.old_ids.append(DisqualificationZone.zone_id)
                        disqualification_zone.save()
                else:
                    disqualification_zone.old_ids = [DisqualificationZone.zone_id]
                    disqualification_zone.save()

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End disqualification_zones ==========================')

    def sync_menu_zones():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ menu_zones ===============================')
        query = MenuZones.objects.using('sitelfl').exclude(menu_zone_id__in = map(lambda x: x.old_id, Menu_zones.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())

        for menu_item in query:
            with transaction.atomic():
                Menu_zones.objects.update_or_create(
                    old_id = menu_item.menu_zone_id,
                    defaults = dict(
                        zone = Disqualification_zones.objects.getOr(old_ids = [menu_item.zone_id], alternative = Disqualification_zones.unknown),
                        menu = Menu.objects.getOr(old_id = menu_item.menu_id, alternative = Menu.unknown),
                        type = Menu_zone_types.objects.get_or_create(code = menu_item.zone_type, defaults = dict(name = menu_item.zone_type))[0],
                    )
                )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End menu_zones ==========================')

    def sync_shirts():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ shirts ===============================')
        ShirtsQuery = Shirts.objects.using('sitelfl').exclude(shirt_id__in = get_ids_from_old_ids(model = Clothes))
        pbar = tqdm(total = ShirtsQuery.count())
        clothes_type, created = Clothes_type.objects.update_or_create(code = 'shirts', defaults = dict(name = 'shirts'))

        for shirt in ShirtsQuery:
            props = 0
            with transaction.atomic():
                if shirt.active == 1:
                    props |= Clothes.props.active

                cloth = Clothes.objects.getOptional(code = f'{shirt.name}_{clothes_type.id}')

                if cloth is None:
                    cloth, created = Clothes.objects.update_or_create(
                        old_ids__overlap = [shirt.shirt_id],
                        clothes_type = clothes_type,
                        defaults = dict(
                            editor = Administrators.objects.get_user(shirt.edited_by_id),
                            code = f'{shirt.name}_{clothes_type.id}',
                            name = shirt.name,
                            props = props
                        )
                    )
                else:
                    created = False

                if created is False:
                    if shirt.shirt_id not in cloth.old_ids:
                        cloth.old_ids.append(shirt.shirt_id)
                        cloth.save()
                else:
                    cloth.old_ids = [shirt.shirt_id]
                    cloth.save()

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End shirts ==========================')

    def sync_shirts_images():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ shirts_images ===============================')
        ShirtImagesQuery = ShirtImages.objects.using('sitelfl').exclude(image_id__in = map(lambda x: x.old_id, Clothes_images.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = ShirtImagesQuery.count())
        clothes_type, _ = Clothes_type.objects.update_or_create(code = f'shirts', defaults = dict(name = f'shirts'))

        for shirt_image in ShirtImagesQuery:
            with transaction.atomic():

                main_model = Clothes.objects.getOr(old_ids__overlap = [shirt_image.shirt_id], clothes_type = clothes_type, alternative = Clothes.unknown)
                props = 0
                if shirt_image.active == 1:
                    props |= Clothes_images.props.active

                clothes_images = Clothes_images.update_or_create_image(
                    file_name = shirt_image.value,
                    main_model = main_model,
                    keyimage = f'shirts_{shirt_image.position}',
                    exception = False,
                    path = 'shirts',
                    defaults = dict(props = props, position = shirt_image.position)
                )

                for clothes_image in clothes_images:
                    clothes_image.old_id = shirt_image.image_id
                    clothes_image.save()

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End shirts_images ==========================')

    def sync_persons():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ persons ===============================')
        OldPersonsQuery = OldPersons.objects.using('sitelfl').filter().exclude(person_id__in = get_ids_from_old_ids(model = Persons))

        pbar = tqdm(total = OldPersonsQuery.count())
        for OldPerson in OldPersonsQuery:
            props = 0
            with transaction.atomic():

                if OldPerson.active == 1:
                    props |= Persons.props.active

                if OldPerson.archive == 1:
                    props |= Persons.props.archive

                birthday = StrToDate(OldPerson.birthday)

                region = Regions.objects.getOr(old_id = OldPerson.region_id, alternative = Regions.unknown)

                user, created_user = User.objects.get_or_create(  # !!! get_or_create не менять
                    last_name = OldPerson.family_name,
                    first_name = OldPerson.first_name,
                    middle_name = OldPerson.second_name,
                    birthday = birthday,
                )

                Users_regions.objects.update_or_create(user = user, defaults = dict(region = region))

                person, created_person = Persons.objects.update_or_create(
                    user = user,
                    defaults = dict(
                        description = OldPerson.admin_comment,
                        props = props,
                        creator = Administrators.objects.get_user(OldPerson.created_by) if OldPerson.created_by is not None else None,
                        editor = Administrators.objects.get_user(OldPerson.edited_by_id) if OldPerson.edited_by_id is not None else None,
                    )
                )

                if person.old_ids is None:
                    person.old_ids = [OldPerson.person_id]
                    if Persons.objects.filter(old_ids__overlap = [OldPerson.person_id]).count() == 0:
                        person.save()
                    else:
                        person.delete()
                elif OldPerson.person_id not in person.old_ids:
                    person.old_ids.append(OldPerson.person_id)
                    person.save()

                Users_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = OldPerson.photo, main_model = person.user, exception = False, keyimage = 'photo', path = 'persons')

                User_e_mails.objects.update_or_create(user = person.user, code = 'email', defaults = dict(e_mail = OldPerson.email))
                User_e_mails.objects.update_or_create(user = person.user, code = 'email2', defaults = dict(e_mail = OldPerson.email2))
                User_phones.objects.update_or_create(user = person.user, code = 'telephone', defaults = dict(phone = OldPerson.telephone))
                User_phones.objects.update_or_create(user = person.user, code = 'telephone2', defaults = dict(phone = OldPerson.telephone2))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End persons ==========================')

    def sync_person_photos():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ person_photos ===============================')

        personQuery = PersonPhotos.objects.using('sitelfl').exclude(person_id__in = get_ids_from_old_ids(model = Users_images)).values('person_id').distinct()
        # personQuery = PersonPhotos.objects.using( 'sitelfl' ).values( 'person_id' ).distinct().order_by('person_id')
        pbar = tqdm(total = personQuery.count())

        for person in personQuery:
            # logger.debug( f"person_id: {person.get( 'person_id' )}" )
            personPhotosQuery = PersonPhotos.objects.using('sitelfl').filter(person_id = person.get('person_id')).exclude(person_id__in = get_ids_from_old_ids(model = Users_images))

            idx = 0
            for personPhoto in personPhotosQuery:
                with transaction.atomic():
                    person = Persons.objects.getOr(old_ids__overlap = [personPhoto.person_id], alternative = Persons.unknown)

                    try:
                        users_image = Users_images.objects.get(old_ids__overlap = [personPhoto.person_id])
                        if not personPhoto.person_id in users_image.old_ids:
                            users_image.old_ids.append(personPhoto.person_id)
                            users_image.save()

                    except Users_images.DoesNotExist:
                        if person is not None:
                            users_images = Users_images.update_or_create_image(
                                file_name = personPhoto.image,
                                main_model = person.user,
                                keyimage = f'photo_{idx}',
                                exception = False,
                                path = 'persons')
                            idx += 1

                            for users_image in users_images:
                                if isinstance(users_image.old_ids, list):
                                    if personPhoto.person_id not in users_image.old_ids:
                                        users_image.old_ids.append(personPhoto.person_id)
                                else:
                                    users_image.old_ids = [personPhoto.person_id]
                                users_image.save()

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End person_photos ==========================')

    def sync_clubs():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ clubs ===============================')

        old_ids = []

        def rec_data(oldClub):
            if oldClub.club_id in old_ids:
                raise Exception(f'{oldClub.club_id} уже обработан.')

            props = 0
            if oldClub.active == 1:
                props |= Clubs.props.active
            if oldClub.national == 1:
                props |= Clubs.props.national

            region = Regions.objects.getOr(old_id = oldClub.region_id, alternative = Regions.unknown)
            club, created = Clubs.objects.get_or_create(old_ids__overlap = [oldClub.club_id], defaults = dict(
                code = oldClub.short_name,
                created_date = oldClub.created_date,
                description = oldClub.text,
                editor = Persons.objects.get_user(old_ids = oldClub.edited_by_id),
                interregion = Interregion.objects.getOr(old_id = oldClub.interregion, alternative = Interregion.unknown),
                league = Leagues.objects.getOr(old_id = oldClub.league_id, alternative = Leagues.unknown),
                name = oldClub.name,
                props = props,
                old_superclub_id = oldClub.superclub,
                region = region,
            ));

            if club.old_ids is None:
                club.old_ids = [oldClub.club_id]
                club.save()

            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.logo1, main_model = club, keyimage = 'logo1', exception = False, path = 'clubs')
            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.logo2, main_model = club, keyimage = 'logo2', exception = False, path = 'clubs')
            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.photo, main_model = club, keyimage = 'photo', exception = False, path = 'clubs')

            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt150_1, main_model = club, keyimage = 'shirt150_1', exception = False, path = 'clubs')
            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt150_2, main_model = club, keyimage = 'shirt150_2', exception = False, path = 'clubs')
            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt150_3, main_model = club, keyimage = 'shirt150_3', exception = False, path = 'clubs')
            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt150_4, main_model = club, keyimage = 'shirt150_4', exception = False, path = 'clubs')

            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt40_1, main_model = club, keyimage = 'shirt40_1', exception = False, path = 'clubs')
            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt40_2, main_model = club, keyimage = 'shirt40_2', exception = False, path = 'clubs')
            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt40_3, main_model = club, keyimage = 'shirt40_3', exception = False, path = 'clubs')
            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt40_4, main_model = club, keyimage = 'shirt40_4', exception = False, path = 'clubs')

            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt_keeper1, main_model = club, keyimage = 'shirt_keeper1', exception = False, path = 'clubs')
            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt_keeper2, main_model = club, keyimage = 'shirt_keeper2', exception = False, path = 'clubs')

            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt_winter1, main_model = club, keyimage = 'shirt_winter1', exception = False, path = 'clubs')
            Clubs_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldClub.shirt_winter2, main_model = club, keyimage = 'shirt_winter2', exception = False, path = 'clubs')

            Clubs_links.objects.update_or_create(club = club, code = 'site', defaults = dict(link = oldClub.site))

            Clothes_clubs.objects.update_or_create(club = club, clothes_type = 'shirts', name = 'Основной цвет маек', code = 'shirts', clothes_context = oldClub.shirts)
            Clothes_clubs.objects.update_or_create(club = club, clothes_type = 'shirts', name = 'Второй цвет маек', code = 'shirts2', clothes_context = oldClub.shirts2)

            Clothes_clubs.objects.update_or_create(club = club, clothes_type = 'shirts_winter', code = 'shirts_winter', name = 'Основной цвет зимней формы', clothes_context = oldClub.shirts_winter)
            Clothes_clubs.objects.update_or_create(club = club, clothes_type = 'shirts_winter', code = 'shirts_winter2', name = 'Второй цвет зимней формы', clothes_context = oldClub.shirts_winter2)

            Clothes_clubs.objects.update_or_create(club = club, clothes_type = 'shorts', code = 'shorts', name = 'Основной цвет шорт', clothes_context = oldClub.shorts)
            Clothes_clubs.objects.update_or_create(club = club, clothes_type = 'shorts', code = 'shorts2', name = 'Второй цвет шорт', clothes_context = oldClub.shorts2)

            Clothes_clubs.objects.update_or_create(club = club, clothes_type = 'socks', code = 'socks', name = 'Основной цвет гетр', clothes_context = oldClub.socks)
            Clothes_clubs.objects.update_or_create(club = club, clothes_type = 'socks', code = 'socks2', name = 'Второй цвет гетр', clothes_context = oldClub.socks2)
            return club, created

        ids = []
        with connections['sitelfl'].cursor() as cursor:
            cursor.execute('''select name, region_id, league_id
                                from clubs
                                group by name, region_id, league_id
                                having count(*) > 1''')
            rows = cursor.fetchall()
            pbar = tqdm(total = len(rows))

            for row in rows:
                with transaction.atomic():
                    name, region_id, league_id = row

                    cursor.execute('''select club_id
                                        from clubs
                                        where name = %s
                                          and region_id = %s
                                          and league_id = %s''', [name, region_id, league_id])
                    rows = cursor.fetchall()

                    ids1 = []
                    step = 0
                    club = None
                    for row1 in rows:
                        club_id, = row1

                        OldClubsQuery = OldClubs.objects.using('sitelfl').filter(club_id = club_id)

                        for oldClub in OldClubsQuery:
                            if step == 0:
                                club, created = rec_data(oldClub)
                                step += 1
                            else:
                                pbar.update()
                                continue

                        ids.append(club_id)
                        ids1.append(club_id)

                    for _id in ids1:
                        if club.old_ids is None:
                            club.old_ids = []

                        if _id not in club.old_ids:
                            if _id in old_ids:
                                raise Exception(f'{oldClub.club_id} уже обработан.')
                            old_ids.append(_id)
                            club.old_ids.append(_id)

                    club.save()

                pbar.update()

        OldClubsQuery = OldClubs.objects.using('sitelfl').exclude(club_id__in = get_ids_from_old_ids(model = Clubs)).exclude(club_id__in = ids)
        pbar = tqdm(total = OldClubsQuery.count())
        for oldClub in OldClubsQuery:
            with transaction.atomic():
                rec_data(oldClub)
            pbar.update()

        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End clubs ==========================')

    def sync_club_contacts():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ club_contacts ===============================')
        ClubContactsQuery = ClubContacts.objects.using('sitelfl').exclude(club_id__in = get_ids_from_old_ids(model = Club_contacts))
        pbar = tqdm(total = ClubContactsQuery.count())
        for oldClubContact in ClubContactsQuery:
            props = 0
            if oldClubContact.active == 1:
                props |= Club_contacts.props.active

            if oldClubContact.leader == 1:
                props |= Club_contacts.props.leader

            try:
                club_contact = Club_contacts.objects.get(
                    club = Clubs.objects.getOr(old_ids__overlap = [oldClubContact.club_id], alternative = Clubs.unknown),
                    editor = Administrators.objects.get_user(oldClubContact.edited_by_id),
                    person = Persons.objects.getOr(old_ids__overlap = [oldClubContact.person_id], alternative = Persons.unknown).user,
                    post = Posts.objects.getOr(code = oldClubContact.post, alternative = Posts.unknown),
                    priority = oldClubContact.priority,
                    props = props,
                )
                if oldClubContact.club_id not in club_contact.old_ids:
                    club_contact.old_ids.append(oldClubContact.club_id)
                    club_contact.save()

            except Club_contacts.DoesNotExist:
                Club_contacts.objects.update_or_create(
                    old_ids = [oldClubContact.club_id],
                    defaults = dict(
                        club = Clubs.objects.getOr(old_ids__overlap = [oldClubContact.club_id], alternative = Clubs.unknown),
                        editor = Administrators.objects.get_user(oldClubContact.edited_by_id),
                        person = Persons.objects.getOr(old_ids__overlap = [oldClubContact.person_id], alternative = Persons.unknown).user,
                        post = Posts.objects.getOr(code = oldClubContact.post, alternative = Posts.unknown),
                        priority = oldClubContact.priority,
                        props = props,
                    )
                )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End club_contacts ==========================')

    def sync_club_admins():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ club_admins ===============================')
        ClubAdminsQuery = ClubAdmins.objects.using('sitelfl').exclude(club_admin_id__in = map(lambda x: x.old_id, Club_admins.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = ClubAdminsQuery.count())
        for oldClubAdmin in ClubAdminsQuery:
            props = 0
            if oldClubAdmin.active == 1:
                props |= Club_admins.props.active

            club, _ = Club_admins.objects.update_or_create(
                old_id = oldClubAdmin.club_admin_id,
                defaults = dict(
                    club = Clubs.objects.getOr(old_ids__overlap = [oldClubAdmin.club_id], alternative = Clubs.unknown),
                    user = Administrators.objects.getOr(old_id = oldClubAdmin.user_id, alternative = Administrators.unknown).user,
                    props = props
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End club_admins ==========================')

    def sync_club_histories():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ club_histories ===============================')
        ClubHistoriesQuery = ClubHistories.objects.using('sitelfl').exclude(name_id__in = map(lambda x: x.old_id, Club_histories.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = ClubHistoriesQuery.count())
        for clubHistory in ClubHistoriesQuery:
            props = 0
            if clubHistory.active == 1:
                props |= Club_histories.props.active

            club = Clubs.objects.getOr(old_ids__overlap = [clubHistory.club_id], alternative = Clubs.unknown)
            Club_histories.objects.update_or_create(
                old_id = clubHistory.name_id,
                defaults = dict(
                    code = f'{clubHistory.name}_{clubHistory.name_id}',
                    club = club,
                    name = clubHistory.name,
                    end_date = clubHistory.end_date,
                    props = props
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End club_histories ==========================')

    def sync_person_club_photos():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ person_club_photos ===============================')

        personQuery = PersonClubPhotos.objects.using('sitelfl'). \
            filter(club_id__isnull = False). \
            exclude(id__in = map(lambda x: x.old_id, Person_club_photos.objects.filter(old_id__isnull = False))). \
            values('person_id', 'club_id').distinct()

        pbar = tqdm(total = personQuery.count())

        for person in personQuery:
            personPhotosQuery = PersonClubPhotos.objects.using('sitelfl'). \
                filter(club_id__isnull = False, person_id = person.get('person_id'), club_id = person.get('club_id')). \
                exclude(id__in = map(lambda x: x.old_id, Person_club_photos.objects.filter(old_id__isnull = False)))

            idx = 0
            for personPhoto in personPhotosQuery:
                props = 0
                with transaction.atomic():
                    if personPhoto.is_main == 1:
                        props |= Person_club_photos.props.main

                    Person_club_photos.update_or_create_image(
                        file_name = personPhoto.photo,
                        main_model = Persons.objects.getOr(old_ids__overlap = [personPhoto.person_id], alternative = Persons.unknown),
                        keyimage = f"photo_{person.get('club_id')}_{idx}",
                        path = 'persons',
                        exception = False,
                        defaults = dict(
                            club = Clubs.objects.getOr(old_ids__overlap = [personPhoto.club_id], alternative = Clubs.unknown),
                            num = personPhoto.num,
                            props = props,
                            old_id = personPhoto.id
                        )
                    )
                    idx += 1

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End person_club_photos ==========================')

    def sync_fields():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ fields ===============================')
        OldFieldsQuery = OldFields.objects.using('sitelfl').exclude(field_id__in = map(lambda x: x.old_id, Fields.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = OldFieldsQuery.count())
        for oldField in OldFieldsQuery:
            with transaction.atomic():
                props = 0
                if oldField.active == 1:
                    props |= Fields.props.active

                field, _ = Fields.objects.update_or_create(
                    old_id = oldField.field_id,
                    defaults = dict(
                        props = props,
                        name = oldField.name,
                        sizes = [oldField.height, oldField.width]
                    )
                )

                Fields_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldField.image, main_model = field, keyimage = 'image', exception = True, path = 'fields')

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End fields ==========================')

    def sync_stadiums():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ stadiums ===============================')
        OldStadiumsQuery = OldStadiums.objects.using('sitelfl').exclude(stadium_id__in = get_ids_from_old_ids(model = Stadiums))
        pbar = tqdm(total = OldStadiumsQuery.count())
        for OldStadium in OldStadiumsQuery:
            with transaction.atomic():
                props = 0
                if OldStadium.active == 1:
                    props |= Stadiums.props.active

                stadium = Stadiums.objects.getOptional(code = AuditModel.translit(OldStadium.name), old_ids = None)
                if stadium is not None:
                    stadium.old_ids = [OldStadium.stadium_id]
                    stadium.save()
                else:
                    stadium, _ = Stadiums.objects.update_or_create(
                        old_ids__overlap = [OldStadium.stadium_id],
                        defaults = dict(
                            region = Regions.objects.getOr(old_id = OldStadium.region_id, alternative = Regions.unknown),
                            name = OldStadium.name,
                            description = OldStadium.description,
                            props = props,
                        )
                    )

                Stadiums_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = OldStadium.logo, main_model = stadium, keyimage = 'logo', exception = False, path = 'stadiums')
                Stadiums_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = OldStadium.plan, main_model = stadium, keyimage = 'plan', exception = False, path = 'stadiums')
                Stadiums_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = OldStadium.photo, main_model = stadium, keyimage = 'photo', exception = False, path = 'stadiums')

                Stadiums_text_informations.objects.update_or_create(stadium = stadium, code = 'address', defaults = dict(text = OldStadium.address))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End stadiums ==========================')

    def sync_stadium_zones():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ stadium_zones ===============================')
        StadiumZonesQuery = StadiumZones.objects.using('sitelfl')

        pbar = tqdm(total = StadiumZonesQuery.count())

        for OldStadium in StadiumZonesQuery:
            Stadium_zones.objects.get_or_create(
                old_stadium_id = OldStadium.stadium_id,
                old_league_id = OldStadium.league_id,
                defaults = dict(
                    league = Leagues.objects.getOr(old_id = OldStadium.league_id, alternative = Leagues.unknown),
                    stadium = Stadiums.objects.getOr(old_ids__overlap = [OldStadium.stadium_id], alternative = Stadiums.unknown)
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End stadium_zones ==========================')

    def sync_contacts():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ contacts ===============================')
        OldContactsQuery = OldContacts.objects.using('sitelfl').exclude(contact_id__in = get_ids_from_old_ids(model = Contacts))
        pbar = tqdm(total = OldContactsQuery.count())

        for OldContact in OldContactsQuery:
            with transaction.atomic():
                try:
                    user = User.objects.getOr(
                        first_name = OldContact.first_name,
                        last_name = OldContact.family_name,
                        middle_name = OldContact.second_name,
                        alternative = User.unknown
                    )
                except User.MultipleObjectsReturned:
                    user = User.unknown()

                club = Clubs.objects.getOr(old_ids__overlap = [OldContact.club_id], alternative = Clubs.unknown)

                try:
                    contact = Contacts.objects.get(
                        user = user,
                        club = club
                    )

                    if not OldContact.contact_id in contact.old_ids:
                        contact.old_ids.append(OldContact.contact_id)
                        contact.save()

                except Contacts.DoesNotExist:
                    contact, created = Contacts.objects.update_or_create(
                        old_ids__overlap = [OldContact.contact_id],
                        defaults = dict(
                            user = user,
                            club = club
                        )
                    )

                    if created and contact.old_ids is None:
                        contact.old_ids = [OldContact.contact_id]
                        contact.save()

                Contacts_e_mails.objects.update_or_create(contact = contact, code = 'email', props = User_e_mails.props.main, defaults = dict(e_mail = OldContact.email))
                Contacts_phones.objects.update_or_create(contact = contact, code = 'telephone', defaults = dict(phone = OldContact.telephone))
                Contacts_phones.objects.update_or_create(contact = contact, code = 'mobile', props = Contacts_phones.props.main, defaults = dict(phone = OldContact.mobile))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End contacts ==========================')

    def sync_players():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ players ===============================')
        OldPlayersQuery = OldPlayers.objects.using('sitelfl').exclude(player_id__in = map(lambda x: x.old_id, Player_old_ids.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = OldPlayersQuery.count())
        cnt = 0

        for OldPlayer in OldPlayersQuery:
            with transaction.atomic():
                if OldPlayer.person_id != 0:
                    person = Persons.objects.getOptionalExt(
                        old_ids__overlap = [OldPlayer.person_id],
                        old_id = OldPlayer.person_id,
                        birthday = OldPlayer.birthday1,
                        first_name = OldPlayer.first_name1,
                        last_name = OldPlayer.family_name1,
                        middle_name = OldPlayer.second_name1,
                        region = Regions.objects.getOr(old_id = OldPlayer.region_id, alternative = Regions.unknown)
                    )
                else:
                    person = Persons.objects.getOr(old_ids__overlap = [OldPlayer.person_id], alternative = Persons.unknown)

                cnt += 1

                props = 0
                if OldPlayer.active == 1:
                    props |= Players.props.active
                if OldPlayer.shadow == 1:
                    props |= Players.props.shadow
                if OldPlayer.blocked == 1:
                    props |= Players.props.blocked
                if OldPlayer.disqualification == 1:
                    props |= Players.props.disqualification
                if OldPlayer.lockout == 1:
                    props |= Players.props.lockout
                if OldPlayer.delayed_lockout == 1:
                    props |= Players.props.delayed_lockout
                if OldPlayer.medical_lockout == 1:
                    props |= Players.props.medical_lockout

                editor = Administrators.objects.getOptional(old_id = OldPlayer.edited_by_id)

                try:
                    club = Clubs.objects.getOr(old_ids__overlap = [OldPlayer.club_id_now], alternative = Clubs.unknown)
                except Clubs.MultipleObjectsReturned:
                    for club in Clubs.objects.filter(old_ids__overlap = [OldPlayer.club_id_now]):
                        if len(club.old_ids) > 1:
                            club.old_ids = list(filter(lambda x: x != OldPlayer.club_id_now, club.old_ids))
                            club.save()
                    club = Clubs.objects.getOr(old_ids__overlap = [OldPlayer.club_id_now], alternative = Clubs.unknown)

                player, created = Players.objects.update_or_create(
                    person = person,
                    defaults = dict(
                        amplua = Posts.objects.update_or_create(code = OldPlayer.amplua, defaults = dict(name = OldPlayer.amplua))[0],
                        club = club,
                        debut = OldPlayer.debut,
                        delayed_lockout_date = OldPlayer.delayed_lockout_date,
                        editor = editor.user if editor is not None else None,
                        height = OldPlayer.height,
                        included = OldPlayer.included,
                        medical_admission_date = OldPlayer.medical_admission_date,
                        number = OldPlayer.number,
                        weight = OldPlayer.weight,
                    )
                )

                Player_old_ids.objects.update_or_create(player = player, old_id = OldPlayer.player_id)

                Players_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = OldPlayer.photo11, main_model = player, keyimage = 'photo11', exception = False, path = 'players')
                Players_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = OldPlayer.photo2, main_model = player, keyimage = 'photo2', exception = False, path = 'players')
                Players_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = OldPlayer.photo3, main_model = player, keyimage = 'photo3', exception = False, path = 'players')

                Players_text_informations.objects.update_or_create(player = player, code = 'lockout_reason', defaults = dict(text = OldPlayer.lockout_reason))
                Players_text_informations.objects.update_or_create(player = player, code = 'delayed_lockout_reason', defaults = dict(text = OldPlayer.delayed_lockout_reason))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End players ==========================')

    def sync_players_change_history():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ players_change_history ===============================')
        Query = PlayersChangeHistory.objects.using('sitelfl')
        pbar = tqdm(total = Query.count())

        for item in Query:
            with transaction.atomic():
                editor = Administrators.objects.getOr(old_id = item.editor_id, alternative = Administrators.unknown)
                try:
                    player = OldPlayers.objects.using('sitelfl').get(player_id = item.player_id)
                except OldPlayers.DoesNotExist:
                    player = None

                if player is not None:
                    player = Player_old_ids.objects.get(old_id = player.player_id).player

                if editor is not None and player is not None:
                    player_change_history, _ = Players_change_history.objects.update_or_create(
                        date_old = item.date,
                        editor_id_old = item.editor_id,
                        player_id_old = item.player_id,
                        defaults = dict(
                            date = item.date,
                            editor = editor.user,
                            player = player
                        )
                    )
                    Players_change_history_text_informations.objects.update_or_create(player_change_history = player_change_history, code = 'data', defaults = dict(text = item.data))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End players_change_history ==========================')

    def sync_referees():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ referees ===============================')
        OldRefereesQuery = OldReferees.objects.using('sitelfl').exclude(referee_id__in = get_ids_from_old_ids(model = Referees))
        pbar = tqdm(total = OldRefereesQuery.count())
        for OldReferee in OldRefereesQuery:
            with transaction.atomic():

                props = 0
                if OldReferee.active == 1:
                    props |= Referees.props.active

                person = Persons.objects.getOptional(old_ids__overlap = [OldReferee.person_id], )
                if person is None:
                    person = Persons.objects.getOptionalExt(
                        old_ids__overlap = [OldReferee.person_id],
                        birthday = OldReferee.birthday1,
                        last_name = OldReferee.family_name1,
                        first_name = OldReferee.first_name1,
                        middle_name = OldReferee.second_name1,
                        region = Regions.objects.getOr(old_id = OldReferee.region_id, alternative = Regions.unknown)
                    )

                referee_post, _ = Posts.objects.update_or_create(code = OldReferee.referee_post if OldReferee.referee_post else unknown, defaults = dict(name = OldReferee.referee_post))

                referee = Referees.objects.getOptional(person = person)

                if referee is None:
                    referee, _ = Referees.objects.update_or_create(
                        old_ids__overlap = [OldReferee.referee_id],
                        defaults = dict(
                            person = person,
                            referee_post = referee_post,
                            contact = Contacts.objects.getOr(old_ids__overlap = [OldReferee.contact_id], alternative = Contacts.unknown),
                            debut = OldReferee.debut,
                            props = props
                        )
                    )

                    if referee.old_ids is None:
                        referee.old_ids = [OldReferee.referee_id]
                        referee.save()

                elif not OldReferee.referee_id in referee.old_ids:
                    referee.old_ids.append(OldReferee.referee_id)
                    referee.save()

                Referees_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = OldReferee.photo11, main_model = referee, keyimage = 'photo11', exception = False, path = 'referees')
                Referees_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = OldReferee.photo2, main_model = referee, keyimage = 'photo2', exception = False, path = 'referees')
                Referees_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = OldReferee.photo3, main_model = referee, keyimage = 'photo3', exception = False, path = 'referees')

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End referees ==========================')

    def sync_referee_zone():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ referee_zone ===============================')
        RefereeZoneQuery = RefereeZone.objects.using('sitelfl').exclude(referee_id__in = map(lambda x: x.old_id, Referee_zone.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = RefereeZoneQuery.count())
        for OldReferee in RefereeZoneQuery:
            Referee_zone.objects.update_or_create(
                old_id = OldReferee.referee_id,
                defaults = dict(
                    referee = Referees.objects.getOr(old_ids__overlap = [OldReferee.referee_id], alternative = Referees.unknown),
                    league = Leagues.objects.getOr(old_id = OldReferee.league_id, alternative = Leagues.unknown)
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End referee_zone ==========================')

    def sync_referee_category():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ referee_category ===============================')
        RefereeCategoryQuery = RefereeCategory.objects.using('sitelfl').exclude(referee_category_id__in = map(lambda x: x.old_id, Referee_category.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = RefereeCategoryQuery.count())
        for refereeCategory in RefereeCategoryQuery:
            props = 0
            if refereeCategory.active == 1:
                props |= Referee_category.props.active

            Referee_category.objects.update_or_create(
                old_id = refereeCategory.referee_category_id,
                defaults = dict(
                    region = Regions.objects.get(old_id = refereeCategory.region_id),
                    props = props,
                    name = refereeCategory.name,
                    priority = refereeCategory.priority,
                )

            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End referee_category ==========================')

    def sync_formation():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ formation ===============================')
        Query = OldFormation.objects.using('sitelfl').exclude(formation_id__in = map(lambda x: x.old_id, Formation.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = Query.count())

        for item in Query:
            props = 0
            if item.active == 1:
                props |= Formation.props.active

            player_change_history, _ = Formation.objects.update_or_create(
                old_id = item.formation_id,
                defaults = dict(
                    description = item.formation,
                    editor = Administrators.objects.get_user(old_id = item.edited_by_id),
                    code = f'{item.name}_{item.priority}',
                    name = item.name,
                    number_of_players = item.number_of_players,
                    priority = StrToNumber(item.priority, default_blank = None),
                    props = props,
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End formation ==========================')

    def sync_fines():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ fines ===============================')
        Query = OldFines.objects.using('sitelfl').exclude(fine_id__in = map(lambda x: x.old_id, Fines.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = Query.count())

        for item in Query:
            with transaction.atomic():
                props = 0
                if item.active == 1:
                    props |= Fines.props.active

                fine, _ = Fines.objects.update_or_create(
                    old_id = item.fine_id,
                    defaults = dict(
                        club = Clubs.objects.getOr(old_ids__overlap = [item.club_id], alternative = Clubs.unknown),
                        kdk = News.objects.getOr(old_id = item.kdk_id, alternative = News.unknown),
                        date = item.date,
                        deliting = IntToBool(item.deleting),
                        editor = Administrators.objects.get_user(item.edited_by_id),
                        lastmodified = item.last_edit_date if isinstance(item.last_edit_date, date) else timezone.now(),
                        payment = item.payment,
                        props = props,
                        remove_restore_date = item.remove_restore_date,
                        sum = item.sum,
                    )
                )

                Fines_text_informations.objects.update_or_create(fine = fine, code = 'comment', defaults = dict(text = item.comment))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End fines ==========================')

    def sync_divisions():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ divisions ===============================')
        Query = OldDivisions.objects.using('sitelfl').exclude(division_id__in = map(lambda x: x.old_id, Divisions.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = Query.count())

        for item in Query:
            props = 0
            if item.active == 1:
                props |= Divisions.props.active
            if item.completed == 1:
                props |= Divisions.props.completed
            if item.show_news == 1:
                props |= Divisions.props.show_news

            division, _ = Divisions.objects.update_or_create(
                old_id = item.division_id,
                defaults = dict(
                    disqualification_condition = Disqualification_condition.objects.update_or_create(code = item.disqualification_condition, defaults = dict(name = item.disqualification_condition))[0],
                    editor = Administrators.objects.get_user(old_id = item.edited_by_id),
                    lastmodified = item.last_edit_date if item.last_edit_date is not None else timezone.now(),
                    number_of_rounds = item.number_of_rounds,
                    name = item.name,
                    scheme = item.scheme,
                    top_text = item.top_text,
                    props = props,
                    region = Regions.objects.getOr(old_id = item.region_id, alternative = Regions.unknown),
                    zone = Disqualification_zones.objects.getOr(old_ids__overlap = [item.zone_id], alternative = Disqualification_zones.unknown)
                )
            )
            Divisions_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = item.scheme, main_model = division, keyimage = 'scheme', exception = False, path = 'divisions')
            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End divisions ==========================')

    def sync_tournaments():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ tournaments ===============================')
        OldTournamentsQuery = OldTournaments.objects.using('sitelfl').exclude(tournament_id__in = map(lambda x: x.old_id, Tournaments.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = OldTournamentsQuery.count())
        for oldTournament in OldTournamentsQuery:
            with transaction.atomic():

                props = 0
                if oldTournament.active == 1:
                    props |= Tournaments.props.active
                if oldTournament.national == 1:
                    props |= Tournaments.props.national
                if oldTournament.show_league == 1:
                    props |= Tournaments.props.show_league
                if oldTournament.show_region == 1:
                    props |= Tournaments.props.show_region
                if oldTournament.calendar_created == 1:
                    props |= Tournaments.props.calendar_created
                if oldTournament.show_numbers == 1:
                    props |= Tournaments.props.show_numbers
                if oldTournament.show_player_number == 1:
                    props |= Tournaments.props.show_player_number
                if oldTournament.show_stats == 1:
                    props |= Tournaments.props.show_stats
                if oldTournament.show_empty_cells == 1:
                    props |= Tournaments.props.show_empty_cells

                editor = Administrators.objects.getOptional(old_id = oldTournament.edited_by_id) if oldTournament.edited_by_id is not None else None

                from lfl_admin.competitions.models.technical_defeat import Technical_defeat
                from lfl_admin.competitions.models.rating_rule import Rating_rule
                tournament, _ = Tournaments.objects.update_or_create(
                    old_id = oldTournament.tournament_id,
                    defaults = dict(
                        code = oldTournament.short_name,
                        disqualification_condition = Disqualification_condition.objects.update_or_create(code = oldTournament.disqualification_condition, defaults = dict(name = oldTournament.disqualification_condition))[0],
                        division = Divisions.objects.getOr(old_id = oldTournament.division_id, alternative = Divisions.unknown),
                        division_priority = oldTournament.division_priority,
                        division_round = oldTournament.division_round,
                        editor = editor.user if editor is not None else None,
                        field = Fields.objects.getOr(old_id = oldTournament.field_id, alternative = Fields.unknown),
                        league = Leagues.objects.getOr(old_id = oldTournament.league_id, alternative = Leagues.unknown),
                        name = oldTournament.name,
                        number_of_players = oldTournament.number_of_players,
                        number_of_rounds = oldTournament.number_of_rounds,
                        number_of_teams = oldTournament.number_of_teams,
                        number_of_tours = oldTournament.number_of_tours,
                        up_selected = oldTournament.up_selected,
                        up2_selected = oldTournament.up2_selected,
                        down_selected = oldTournament.down_selected,
                        down2_selected = oldTournament.down2_selected,
                        priority = oldTournament.priority,
                        props = props,
                        protocol_type = Protocol_types.objects.update_or_create(code = oldTournament.protocol_type, defaults = dict(name = oldTournament.protocol_type))[0],
                        rating_rule = Rating_rule.objects.update_or_create(code = oldTournament.rating_rule, defaults = dict(name = oldTournament.rating_rule))[0],
                        referee_category = Referee_category.objects.getOr(old_id = oldTournament.referee_category_id, alternative = Referee_category.unknown),
                        referees_max = oldTournament.referees_max,
                        region = Regions.objects.getOr(old_id = oldTournament.region_id, alternative = Regions.unknown),
                        season = Seasons.objects.getOr(old_id = oldTournament.season_id, alternative = Seasons.unknown),
                        start_date = oldTournament.start_date,
                        statistics_type = Statistics_types.objects.update_or_create(code = oldTournament.statistics_type, defaults = dict(name = oldTournament.statistics_type))[0],
                        technical_defeat = Technical_defeat.objects.update_or_create(code = oldTournament.technical_defeat, defaults = dict(name = oldTournament.technical_defeat))[0],
                        tournament_type = Tournament_types.objects.update_or_create(code = oldTournament.tournament_type, defaults = dict(name = oldTournament.tournament_type))[0],
                        zone = Disqualification_zones.objects.getOr(old_ids__overlap = [oldTournament.zone_id], alternative = Disqualification_zones.unknown),

                    )
                )

                Tournaments_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldTournament.logo, main_model = tournament, keyimage = 'logo', exception = False, path = 'tournaments')
                Tournaments_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = oldTournament.scheme, main_model = tournament, keyimage = 'scheme', exception = False, path = 'tournaments')

            pbar.update()

        restruct_divisions()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End tournaments ==========================')

    def sync_cards():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ cards ===============================')
        query = OldCards.objects.using('sitelfl').exclude(card_id__in = map(lambda x: x.old_id, Cards.objects.filter(old_id__isnull = False)))
        # query = OldCards.objects.using( 'sitelfl' )
        pbar = tqdm(total = query.count())

        for item in query:
            Cards.objects.update_or_create(
                old_id = item.card_id,
                defaults = dict(
                    card_type = Card_types.objects.update_or_create(code = item.card_type, defaults = dict(name = item.card_type))[0],
                    club = Clubs.objects.getOr(old_ids__overlap = [item.club_id], alternative = Clubs.unknown),
                    match = Calendar.objects.getOr(old_id = item.match_id, alternative = Calendar.unknown),
                    minute = item.minute,
                    player = Player_old_ids.get_payer_from_old_player(old_player_id = item.player_id),
                    referee = Referees.objects.getOr(old_ids__overlap = [item.referee_id], alternative = Referees.unknown),
                    tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End cards ==========================')

    def sync_disqualifications():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ disqualifications ===============================')
        Query = OldDisqualifications.objects.using('sitelfl').exclude(disqualification_id__in = map(lambda x: x.old_id, Disqualifications.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = Query.count())

        for item in Query:
            with transaction.atomic():
                props = 0
                if item.active == 1:
                    props |= Disqualifications.props.active

                if item.disqualification_type is None:
                    disqualification_type = Disqualification_types.unknown()
                else:
                    disqualification_type, _ = Disqualification_types.objects.update_or_create(code = item.disqualification_type, defaults = dict(name = item.disqualification_type))

                Disqualifications.objects.update_or_create(
                    old_id = item.disqualification_id,
                    defaults = dict(
                        admin = Administrators.objects.getOr(old_id = item.admin_id, alternative = Administrators.unknown).user if item.admin_id is not None else Administrators.unknown().user,
                        card = Cards.objects.getOr(old_id = item.card_id, alternative = Cards.unknown),
                        disqualification_type = disqualification_type,
                        edit_date = item.edit_date,
                        from_date = item.from_date,
                        to_date = item.to_date,
                        matches = item.matches,
                        personal_league = Leagues.objects.getOr(old_id = item.personal_league_id, alternative = Leagues.unknown),
                        personal_region = Regions.objects.getOr(old_id = item.personal_region_id, alternative = Regions.unknown),
                        player = Player_old_ids.get_payer_from_old_player(old_player_id = item.player_id),
                        props = props,
                        tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                        zone = Disqualification_zones.objects.getOr(old_ids__overlap = [item.zone_id], alternative = Disqualification_zones.unknown)
                    )
                )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End disqualifications ==========================')

    def sync_keepers():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ keepers ===============================')

        oldQuery = OldKeepers.objects.using('sitelfl')
        cnt = oldQuery.count()
        pbar = tqdm(total = cnt)

        comp_ids = list(map(lambda x: x.old_id, Keepers.objects.filter(old_id__isnull = False)))

        fetcher = lazy_bulk_fetch(100000, cnt, lambda: oldQuery)
        for batch in fetcher:
            query = list(OldKeepers.objects.using('sitelfl').raw(str(batch.query).replace('keepers.', '').replace('"', '')))
            for item in query:
                if item.comp_ids in comp_ids:
                    pbar.update()
                    continue

                Keepers.objects.update_or_create(
                    match_id_old = item.match_id,
                    player_id_old = item.player_id,
                    tournament_id_old = item.tournament_id,
                    defaults = dict(
                        club = Clubs.objects.getOr(old_ids__overlap = [item.club_id], alternative = Clubs.unknown),
                        editor = Administrators.objects.get_user(old_id = item.edited_by_id),
                        goals = item.goals,
                        lastmodified = item.last_edit_date if isinstance(item.last_edit_date, date) else timezone.now(),
                        match = Calendar.objects.getOr(old_id = item.match_id, alternative = Calendar.unknown),
                        player = Player_old_ids.get_payer_from_old_player(old_player_id = item.player_id),
                        tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                    )
                )
                pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End keepers ==========================')

    def sync_fouls():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ fouls ===============================')
        query = OldFouls.objects.using('sitelfl').exclude(foul_id__in = map(lambda x: x.old_id, Fouls.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())

        for item in query:
            props = 0
            if item.penalty == 1:
                props |= Fouls.props.penalty

            fine, _ = Fouls.objects.get_or_create(
                old_id = item.foul_id,
                defaults = dict(
                    club = Clubs.objects.getOr(old_ids__overlap = [item.club_id], alternative = Clubs.unknown),
                    editor = Administrators.objects.get_user(item.edited_by_id),
                    lastmodified = item.last_edit_date,
                    match = Calendar.objects.getOr(old_id = item.match_id, alternative = Calendar.unknown),
                    minute = item.minute,
                    player = Player_old_ids.get_payer_from_old_player(old_player_id = item.player_id),
                    props = props,
                    tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End fouls ==========================')

    def sync_match_stats():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ match_stats ===============================')
        Query = MatchStats.objects.using('sitelfl').exclude(match_id__in = map(lambda x: x.old_id, Match_stats.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = Query.count())

        for item in Query:
            Match_stats.objects.update_or_create(
                old_id = item.match_id,
                defaults = dict(
                    away_value = item.away_value,
                    home_value = item.home_value,
                    type = Match_stat_types.objects.get_or_create(code = item.stat_key, name = item.stat_title)[0],
                    match = Calendar.objects.getOr(old_id = item.match_id, alternative = Calendar.unknown),
                )
            )
            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End match_stats ==========================')

    def sync_matchdays():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ matchdays ===============================')
        Query = OldMatchdays.objects.using('sitelfl')
        pbar = tqdm(total = Query.count())

        for item in Query:
            Matchdays.objects.update_or_create(
                old_tour = item.tour,
                old_tournament_id = item.tournament_id,
                defaults = dict(
                    date = item.date,
                    code = f'{item.name}_{item.tournament_id}_{item.tour}',
                    name = item.name,
                    tour = item.tour,
                    tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                )
            )
            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End matchdays ==========================')

    def sync_calendar():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ calendar ===============================')
        Query = OldCalendar.objects.using('sitelfl').exclude(match_id__in = map(lambda x: x.old_id, Calendar.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = Query.count())

        for item in Query:
            with transaction.atomic():
                if item.away_score is None:
                    item.away_score = '0'

                if item.home_score is None:
                    item.home_score = '0'

                if item.away_points is None:
                    item.away_points = 0

                if item.home_points is None:
                    item.home_points = 0

                away_score = item.away_score.replace('`', '').replace('п', '').replace('-', '')
                home_score = item.home_score.replace('`', '').replace('п', '').replace('-', '')

                props = 0
                if item.protocol == 1:
                    props |= Calendar.props.protocol
                if item.in_archive == 1:
                    props |= Calendar.props.in_archive
                if item.show_stats == 1:
                    props |= Calendar.props.show_stats
                if item.show_empty_cells == 1:
                    props |= Calendar.props.show_empty_cells
                if item.away_score.find('п') != -1 or item.home_score.find('п') != -1:
                    props |= Calendar.props.penalty

                calendar, _ = Calendar.objects.update_or_create(
                    old_id = item.match_id,
                    defaults = dict(
                        away = Clubs.objects.getOr(old_ids__overlap = [item.away_id], alternative = Clubs.unknown),
                        away_formation = Formation.objects.getOr(old_id = item.away_formation, alternative = Formation.unknown),
                        away_points = item.away_points,
                        away_score = StrToNumber(away_score, 0),
                        checked = item.checked,
                        division = Divisions.objects.getOr(old_id = item.division_id, alternative = Divisions.unknown),
                        editor = Administrators.objects.get_user(item.edited_by_id),
                        home = Clubs.objects.getOr(old_ids__overlap = [item.home_id], alternative = Clubs.unknown),
                        home_formation = Formation.objects.getOr(old_id = item.home_formation, alternative = Formation.unknown),
                        home_points = item.home_points,
                        home_score = StrToNumber(home_score, 0),
                        lastmodified = item.last_edit_date if item.last_edit_date else timezone.now(),
                        league = Leagues.objects.getOr(old_id = item.league_id, alternative = Leagues.unknown),
                        match_date_time = item.match_date_time,
                        match_number = item.match_number,
                        props = props,
                        referee = Referees.objects.getOr(old_ids__overlap = [item.referee_id], alternative = Referees.unknown),
                        season = Seasons.objects.getOr(old_id = item.season_id, alternative = Seasons.unknown),
                        stadium = Stadiums.objects.getOr(old_ids__overlap = [item.stadium_id], alternative = Stadiums.unknown),
                        technical_defeat = item.technical_defeat,
                        tour = item.tour,
                        tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                    )
                )

                Calendar_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = item.away_shirt, main_model = calendar, keyimage = 'away_shirt', exception = False, path = 'calendar')
                Calendar_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = item.away_shirt_keeper, main_model = calendar, keyimage = 'away_shirt_keeper', exception = False, path = 'calendar')

                Calendar_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = item.home_shirt, main_model = calendar, keyimage = 'home_shirt', exception = False, path = 'calendar')
                Calendar_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = item.home_shirt_keeper, main_model = calendar, keyimage = 'home_shirt_keeper', exception = False, path = 'calendar')

                Calendar_text_informations.objects.update_or_create(calendar = calendar, code = 'comment', defaults = dict(text = item.comment))
                Calendar_text_informations.objects.update_or_create(calendar = calendar, code = 'note', defaults = dict(text = item.note))

                Calendar_links.objects.update_or_create(calendar = calendar, code = 'gallery_link', defaults = dict(link = item.gallery_link))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End calendar ==========================')

    def sync_assists():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ assists ===============================')
        Query = OldAssists.objects.using('sitelfl').exclude(assist_id__in = map(lambda x: x.old_id, Assists.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = Query.count())

        for item in Query:
            Assists.objects.update_or_create(
                old_id = item.assist_id,
                defaults = dict(
                    club = Clubs.objects.getOr(old_ids__overlap = [item.club_id], alternative = Clubs.unknown),
                    editor = Administrators.objects.get_user(item.edited_by_id),
                    lastmodified = item.last_edit_date if item.last_edit_date is not None else timezone.now(),
                    match = Calendar.objects.getOr(old_id = item.match_id, alternative = Calendar.unknown),
                    player = Player_old_ids.get_payer_from_old_player(old_player_id = item.player_id),
                    tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown)
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End assists ==========================')

    def sync_tournament_members():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ tournament_members ===============================')
        TournamentMembersQuery = TournamentMembers.objects.using('sitelfl')
        pbar = tqdm(total = TournamentMembersQuery.count())
        for TournamentMember in TournamentMembersQuery:
            club = Clubs.objects.getOr(old_ids__overlap = [TournamentMember.club_id], alternative = Clubs.unknown)

            props = 0
            if TournamentMember.game_over == 1:
                props |= Tournament_members.props.game_over

            Tournament_members.objects.update_or_create(
                tournament_id_old = TournamentMember.tournament_id,
                club_id_old = TournamentMember.club_id,
                defaults = dict(
                    club = club,
                    props = props,
                    position = TournamentMember.position,
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End tournament_members ==========================')

    def sync_tournament_member_doubles():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ tournament_member_doubles ===============================')
        TournamentMemberDoublesQuery = TournamentMemberDoubles.objects.using('sitelfl')
        pbar = tqdm(total = TournamentMemberDoublesQuery.count())

        for TournamentMemberDouble in TournamentMemberDoublesQuery:
            with transaction.atomic():
                club = Clubs.objects.getOr(old_ids__overlap = [TournamentMemberDouble.club_id], alternative = Clubs.unknown)
                club_double = Clubs.objects.getOr(old_ids__overlap = [TournamentMemberDouble.club_double_id], alternative = Clubs.unknown)

                tournament = Tournaments.objects.getOr(old_id = TournamentMemberDouble.tournament_id, alternative = Tournaments.unknown)
                tournament_double = Tournaments.objects.getOr(old_id = TournamentMemberDouble.tournament_double_id, alternative = Tournaments.unknown)

                Tournament_member_doubles.objects.update_or_create(
                    old_id = TournamentMemberDouble.tournament_member_double_id,
                    defaults = dict(
                        club = club,
                        club_double = club_double,
                        tournament = tournament,
                        tournament_double = tournament_double,
                    )
                )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End tournament_member_doubles ==========================')

    def sync_player_histories():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ player_histories ===============================')

        cnt = PlayerHistories.objects.using('sitelfl').count()
        pbar = tqdm(total = cnt)

        fetcher = lazy_bulk_fetch(100000, cnt, lambda: PlayerHistories.objects.using('sitelfl'))
        for batch in fetcher:
            with transaction.atomic():
                query = list(PlayerHistories.objects.using('sitelfl').raw(str(batch.query).replace('player_histories.', '').replace('"', '')))

                for item in query:
                    if Player_histories.objects.getOptional(old_id = item.comp_ids) is not None:
                        pbar.update()
                        continue

                    props = 0

                    if item.game_started == 1:
                        props |= Player_histories.props.game_started

                    if item.substituted == 1:
                        props |= Player_histories.props.substituted

                    if item.keeper == 1:
                        props |= Player_histories.props.keeper

                    player_old_ids = Player_old_ids.objects.getOptional(old_id = item.player_id)
                    if player_old_ids is None:
                        player = Players.unknown()
                    else:
                        player = player_old_ids.player

                    res = Player_histories.objects.getOptional(
                        club_id_old = item.club_id,
                        match_id_old = item.match_id,
                        player_id_old = item.player_id,
                    )

                    if res is None:
                        res, _ = Player_histories.objects.update_or_create(
                            club = Clubs.objects.getOr(old_ids__overlap = [item.club_id], alternative = Clubs.unknown),
                            match = Calendar.objects.getOr(old_id = item.match_id, alternative = Calendar.unknown),
                            player = player,
                            defaults = dict(
                                club_id_old = item.club_id,
                                match_id_old = item.match_id,
                                player_id_old = item.player_id,
                                editor = Administrators.objects.get_user(item.edited_by_id),
                                formation = Formation.objects.getOr(old_id = item.formation, alternative = Formation.unknown),
                                props = props,
                                tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                            )
                        )

                pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End player_histories ==========================')

    def sync_goals():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ goals ===============================')
        query = OldGoals.objects.using('sitelfl').exclude(goal_id__in = map(lambda x: x.old_id, Goals.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())
        for item in query:
            player_old_ids = Player_old_ids.objects.getOptional(old_id = item.player_id)
            if player_old_ids is None:
                player = Players.unknown()
            else:
                player = player_old_ids.player

            res, _ = Goals.objects.get_or_create(
                old_id = item.goal_id,
                defaults = dict(
                    assist = Assists.objects.getOr(old_id = item.assist_id, alternative = Assists.unknown),
                    club = Clubs.objects.getOr(old_ids__overlap = [item.club_id], alternative = Clubs.unknown),
                    goal_club = Clubs.objects.getOr(old_ids__overlap = [item.goal_club_id], alternative = Clubs.unknown),
                    goal_type = Goals_type.objects.update_or_create(code = item.goal_type, defaults = dict(name = item.goal_type))[0],
                    match = Calendar.objects.getOr(old_id = item.match_id, alternative = Calendar.unknown),
                    minute = item.minute,
                    player = player,
                    tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End goals ==========================')

    def sync_penalties():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ penalties ===============================')
        query = OldPenalties.objects.using('sitelfl').exclude(penalty_id__in = map(lambda x: x.old_id, Penalties.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())
        for item in query:
            props = 0
            if item.action == 1:
                props |= Penalties.props.action

            if item.result == 1:
                props |= Penalties.props.result

            player_old_ids = Player_old_ids.objects.getOptional(old_id = item.player_id)
            if player_old_ids is None:
                player = Players.unknown()
            else:
                player = player_old_ids.player

            res, _ = Penalties.objects.update_or_create(
                old_id = item.penalty_id,
                defaults = dict(
                    club = Clubs.objects.getOr(old_ids__overlap = [item.club_id], alternative = Clubs.unknown),
                    editor = Administrators.objects.get_user(item.edited_by_id),
                    match = Calendar.objects.getOr(old_id = item.match_id, alternative = Calendar.unknown),
                    minute = item.minute,
                    player = player,
                    props = props,
                    referee = Referees.objects.getOr(old_ids__overlap = [item.referee_id], alternative = Referees.unknown),
                    tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End penalties ==========================')

    def sync_squads():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ squads ===============================')
        query = OldSquads.objects.using('sitelfl')

        cnt = query.count()
        pbar = tqdm(total = cnt)

        fetcher = lazy_bulk_fetch(100000, cnt, lambda: query)

        for batch in fetcher:
            with transaction.atomic():
                sql_str = str(batch.query).replace('squads.', '').replace('"', '')
                lst = OldSquads.objects.using('sitelfl').raw(sql_str)
                for item in lst:
                    if Squads.objects.getOptional(old_id = item.comp_ids) is not None:
                        pbar.update()
                        continue

                    res, _ = Squads.objects.get_or_create(
                        club_id_old = item.club_id,
                        player_id_old = item.player_id,
                        tournament_id_old = item.tournament_id,
                        defaults = dict(
                            club = Clubs.objects.getOr(old_ids__overlap = [item.club_id], alternative = Clubs.unknown),
                            deducted = item.deducted,
                            editor = Administrators.objects.get_user(item.edited_by_id),
                            included = item.included,
                            old_id = f"{item.player_id}_{item.club_id}_{item.tournament_id}",
                            player = Player_old_ids.objects.get_player(old_id = item.player_id),
                            tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                        )
                    )

                    Squads_text_informations.objects.update_or_create(squad = res, code = 'comment', defaults = dict(text = item.comment))

                    pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End squads ==========================')

    def sync_squads_match():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ squads_match ===============================')
        query = SquadsMatch.objects.using('sitelfl').exclude(squads_match_id__in = map(lambda x: x.old_id, Squads_match.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())
        for item in query:
            res, _ = Squads_match.objects.update_or_create(
                old_id = item.squads_match_id,
                defaults = dict(
                    match = Calendar.objects.getOr(old_id = item.match_id, alternative = Calendar.unknown),
                    number = item.number,
                    player = Player_old_ids.objects.get_player(old_id = item.player_id),
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End squads_match ==========================')

    def sync_news():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ news ===============================')
        query = OldNews.objects.using('sitelfl').exclude(id__in = map(lambda x: x.old_id, News.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())
        for item in query:
            with transaction.atomic():
                props = 0

                if item.active == 1:
                    props |= News.props.active

                if item.disable_editor == 1:
                    props |= News.props.disable_editor

                if item.fixed_position == 1:
                    props |= News.props.fixed_position

                if item.in_bottom == 1:
                    props |= News.props.in_bottom

                if item.in_middle == 1:
                    props |= News.props.in_middle

                if item.in_top == 1:
                    props |= News.props.in_top

                new, _ = News.objects.update_or_create(
                    old_id = item.id,
                    defaults = dict(
                        admin = Administrators.objects.getOr(old_id = item.admin_id, alternative = Administrators.unknown).user if item.admin_id is not None else Administrators.unknown().user,
                        attache_dir = item.attache_dir,
                        created = Administrators.objects.getOr(old_id = item.admin_id, alternative = Administrators.unknown).user if item.admin_id is not None else Administrators.unknown().user,
                        date = item.date,
                        editing = True if item.disable_editor == 0 else False,
                        en = News.objects.getOptional(id = item.en_id),
                        icon = News_icon_type.objects.get_or_create(code = item.icon if item.icon else unknown, defaults = dict(name = item.icon))[0],
                        lastmodified = item.last_edit_date if item.last_edit_date else timezone.now(),
                        league = Leagues.objects.getOr(old_id = item.league_id, alternative = Leagues.unknown),
                        match = Calendar.objects.getOr(old_id = item.match_id, alternative = Calendar.unknown),
                        old_image_big_id = item.image_big_id,
                        old_image_small_id = item.image_small_id,
                        position = item.position,
                        old_tour = item.tour,
                        region = Regions.objects.getOr(old_id = item.region_id, alternative = Regions.unknown),
                        tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                        type = News_type.objects.get_or_create(code = item.type, defaults = dict(name = item.type))[0]
                    )
                )

                News_text_informations.objects.update_or_create(new = new, code = 'comment', defaults = dict(text = item.comment))
                News_text_informations.objects.update_or_create(new = new, code = 'preamble', defaults = dict(text = item.preamble))
                News_text_informations.objects.update_or_create(new = new, code = 'text', defaults = dict(text = item.text))
                News_text_informations.objects.update_or_create(new = new, code = 'title', defaults = dict(text = item.title))

                News_links.objects.update_or_create(new = new, code = 'external_link', defaults = dict(link = item.external_link))
                News_links.objects.update_or_create(new = new, code = 'link', defaults = dict(link = item.link))

                image_big = OldImages.objects.using('sitelfl').getOptional(image_id = item.image_big_id)
                if image_big is not None:
                    News_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = image_big.image_path, main_model = new, keyimage = image_big.type, exception = False, path = 'news')

                image_small = OldImages.objects.using('sitelfl').getOptional(image_id = item.image_small_id)
                if image_small is not None:
                    News_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = image_small.image_path, main_model = new, keyimage = image_small.type, exception = False, path = 'news')

                News_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = item.image_path, main_model = new, keyimage = 'image_path', exception = False, path = 'news')
                News_images.update_or_create_image(o_ssh_client = o_ssh_client, file_name = item.imageshort, main_model = new, keyimage = 'imageshort', exception = False, path = 'news')

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End news ==========================')

    def sync_news_start_block_tournament():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ news_start_block_tournament ===============================')
        query = NewsStartBlockTournament.objects.using('sitelfl').exclude(id__in = map(lambda x: x.old_id, News_start_block_tournament.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())
        for item in query:
            with transaction.atomic():
                props = 0

                if item.active == 1:
                    props |= News.props.active

                if item.disable_editor == 1:
                    props |= News.props.disable_editor

                if item.in_middle == 1:
                    props |= News.props.in_middle

                if item.in_top == 1:
                    props |= News.props.in_top

                block, _ = News_start_block_tournament.objects.update_or_create(
                    old_id = item.id,
                    defaults = dict(
                        admin = Administrators.objects.getOr(old_id = item.admin_id, alternative = Administrators.unknown).user if item.admin_id is not None else Administrators.unknown().user,
                        created = Administrators.objects.getOr(old_id = item.admin_id, alternative = Administrators.unknown).user if item.admin_id is not None else Administrators.unknown().user,
                        date = item.date,
                        editing = True if item.disable_editor == 0 else False,
                        lastmodified = item.last_edit_date if item.last_edit_date else timezone.now(),
                        tournament = Tournaments.objects.getOr(old_id = item.tournament_id, alternative = Tournaments.unknown),
                    )
                )

                News_start_block_tournament_text_informations.objects.update_or_create(block = block, code = 'comment', defaults = dict(text = item.comment))
                News_start_block_tournament_text_informations.objects.update_or_create(block = block, code = 'preamble', defaults = dict(text = item.preamble))

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End news ==========================')

    def sync_news_actions():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ news_actions ===============================')
        query = NewsActions.objects.using('sitelfl').exclude(id__in = map(lambda x: x.old_id, News_actions.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())
        for item in query:
            new = News.objects.getOptional(old_id = item.news_id)
            if new is not None:
                res, _ = News_actions.objects.update_or_create(
                    old_id = item.id,
                    defaults = dict(
                        dt = item.dt,
                        from_data = item.from_data,
                        from_tag = item.from_tag,
                        new = new,
                        to_data = item.to_data,
                        to_tag = item.to_tag,
                        type = News_action_types.objects.get_or_create(code = item.type, defaults = dict(name = item.type))[0],
                        user = Administrators.objects.get_user(old_id = item.user_id, alternative = User.unknown),
                    )
                )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End news_actions ==========================')

    def sync_news_favorites():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ news_favorites ===============================')
        query = NewsFavorites.objects.using('sitelfl').exclude(id__in = map(lambda x: x.old_id, News_favorites.objects.filter(old_id__isnull = False)))
        pbar = tqdm(total = query.count())
        for item in query:
            new = News.objects.getOptional(old_id = item.id)
            admin = Administrators.objects.get_user(old_id = item.admin_id)

            if new is not None and admin is not None:
                res, _ = News_favorites.objects.update_or_create(
                    old_id = item.id,
                    defaults = dict(
                        new = new,
                        admin = admin,
                    )
                )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End news_favorites ==========================')

    def sync_news_quantity_by_url():
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================ news_quantity_by_url ===============================')
        query = NewsQuantityByUrl.objects.using('sitelfl')
        pbar = tqdm(total = query.count())
        for item in query.values('url', 'quantity'):
            res, _ = NewsQuantity_ByUrl.objects.update_or_create(
                url = item.get('url'),
                defaults = dict(
                    quantity = item.get('quantity'),
                )
            )

            pbar.update()
        logger.debug(f'{DateTimeToStr(date = timezone.now(), hours = 3)} ============================= End news_quantity_by_url ==========================')

    try:
        if 'administrators' in modes:
            sync_administrators()

        if 'region_zones' in modes:
            sync_region_zones()

        if 'seasons' in modes:
            sync_seasons()

        if 'cities' in modes:
            sync_cities()

        if 'region' in modes:
            sync_region()

        if 'banners' in modes:
            sync_banners()

        if 'leagues' in modes:
            sync_leagues()

        if 'stadiums' in modes:
            sync_stadiums()

        if 'stadium_rating' in modes:
            sync_stadium_rating()

        if 'stadium_zones' in modes:
            sync_stadium_zones()

        if 'bottom_menu' in modes:
            sync_bottom_menu()

        if 'menu' in modes:
            sync_menu()

        if 'menu_item' in modes:
            sync_menu_items()

        if 'menu_item_league' in modes:
            sync_menu_items_leagues()

        if 'disqualification_zones' in modes:
            sync_disqualification_zones()

        if 'menu_zones' in modes:
            sync_menu_zones()

        if 'shirts' in modes:
            sync_shirts()

        if 'shirts_images' in modes:
            sync_shirts_images()

        if 'persons' in modes:
            sync_persons()

        if 'person_photos' in modes:
            sync_person_photos()

        if 'clubs' in modes:
            sync_clubs()

        if 'club_contacts' in modes:
            sync_club_contacts()

        if 'club_admins' in modes:
            sync_club_admins()

        if 'club_histories' in modes:
            sync_club_histories()

        if 'person_club_photos' in modes:
            sync_person_club_photos()

        if 'fields' in modes:
            sync_fields()

        if 'stadiums' in modes:
            sync_stadiums()

        if 'contacts' in modes:
            sync_contacts()

        if 'players' in modes:
            sync_players()

        if 'players_change_history' in modes:
            sync_players_change_history()

        if 'referees' in modes:
            sync_referees()

        if 'referee_zone' in modes:
            sync_referee_zone()

        if 'referee_category' in modes:
            sync_referee_category()

        if 'formation' in modes:
            sync_formation()

        if 'news' in modes:
            sync_news()

        if 'news_actions' in modes:
            sync_news_actions()

        if 'news_favorites' in modes:
            sync_news_favorites()

        if 'news_quantity_by_url' in modes:
            sync_news_quantity_by_url()

        if 'news_start_block_tournament' in modes:
            sync_news_start_block_tournament()

        if 'fines' in modes:
            sync_fines()

        if 'divisions' in modes:
            sync_divisions()

        if 'tournaments' in modes:
            sync_tournaments()

        if 'cards' in modes:
            sync_cards()

        if 'disqualifications' in modes:
            sync_disqualifications()

        if 'keepers' in modes:
            sync_keepers()

        if 'fouls' in modes:
            sync_fouls()

        if 'match_stats' in modes:
            sync_match_stats()

        if 'matchdays' in modes:
            sync_matchdays()

        if 'calendar' in modes:
            sync_calendar()

        if 'assists' in modes:
            sync_assists()

        if 'tournament_members' in modes:
            sync_tournament_members()

        if 'tournament_member_doubles' in modes:
            sync_tournament_member_doubles()

        if 'player_histories' in modes:
            sync_player_histories()

        if 'goals' in modes:
            sync_goals()

        if 'squads' in modes:
            sync_squads()

        if 'squads_match' in modes:
            sync_squads_match()

        if 'penalties' in modes:
            sync_penalties()

        logger.debug(f'Done. {DateTimeToStr(date = timezone.now(), hours = 3)}')
    except Exception as ex:
        logger.error(ex, exc_info = True)
        raise ex
