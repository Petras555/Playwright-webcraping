import  requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import asyncio
from test_db import Sklypas, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


web ="https://www.aruodas.lt/sklypai-pardavimui/?FOfferType=1&FIntendance=farm&FBuildingType=1"
web_2='https://www.aruodas.lt/sklypai-pardavimui/puslapis/2/?FOfferType=1&FIntendance=farm&FBuildingType=1'
web_3='https://www.aruodas.lt/sklypai-pardavimui/puslapis/3/?FOfferType=1&FIntendance=farm&FBuildingType=1'
url = requests.get(web)

list= []
async def page_switcher(i):
    web_2 = "https://www.aruodas.lt/sklypai-pardavimui/puslapis/"+i+"/?FOfferType=1&FIntendance=farm&FBuildingType=1"
    return web_2


async def scrape(x, y, z):
    await x.goto(y)
    if z == 1:
        await x.locator('xpath=//*[@id="onetrust-accept-btn-handler"]').click();


    all_items = await x.query_selector('.list-search')

    blocks = await all_items.query_selector_all('''.list-row
                                        ''')
    for block in blocks:
        try:
            dict = {}
            name = await block.query_selector('.list-adress ')
            name2 = await name.query_selector('a')
            name_txt = await name2.text_content()
            dict['Pavadinimas'] = name_txt.strip()
            name_db = name_txt.strip()
        except AttributeError:
            continue

        try:

            price = await block.query_selector('.list-item-price')
            price_txt = await price.text_content()
            dict['Kaina'] = price_txt
            price_fix = price_txt.replace('€', '').strip()
            price_fix_2 = price_fix.replace(' ', '')
            price_db = float(price_fix_2)
        except AttributeError:
            continue

        try:
            area = await block.query_selector('.list-AreaOverall')
            area_txt = await area.text_content()
            dict['Plotas'] = area_txt.strip()
            list.append(dict)
            area_fix = area_txt.strip()
            area_db = float(area_txt)
        except AttributeError:
            continue

        sklypas = Sklypas(name_db, price_db, area_db)
        session.add(sklypas)
        session.commit()

    for i in list:
        print(i)

async def main():
    async with async_playwright() as pw:
        browser = await pw.firefox.launch(headless=False)
        page = await browser.new_page()

        await scrape(page, web, 1)
        for num in range(2,5):
            str_num = str(num)
            await scrape(page, await page_switcher(str(num)), 0)


        await browser.close()



asyncio.run(main())

