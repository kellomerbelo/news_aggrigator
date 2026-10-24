import json
import logging
import requests
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
import feedparser

# Configure Logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")
logger = logging.getLogger("haberdakika")

RSS_FEEDS = [
    {"name": "Hürriyet", "url": "https://www.hurriyet.com.tr/rss/anasayfa"},
    {"name": "Sözcü", "url": "https://www.sozcu.com.tr/rss"},
    {"name": "Sabah", "url": "https://www.sabah.com.tr/rss/anasayfa.xml"},
    {"name": "CNN Türk", "url": "https://www.cnnturk.com/feed/rss/all/news"},
    {"name": "Habertürk", "url": "https://www.haberturk.com/rss"},
    {"name": "NTV", "url": "https://www.ntv.com.tr/son-dakika.rss"},
    {"name": "TRT Haber", "url": "https://www.trthaber.com/xml_feed.xml"},
    {"name": "Anadolu Ajansı", "url": "https://www.aa.com.tr/tr/rss/default"},
    {"name": "Milliyet", "url": "https://www.milliyet.com.tr/rss/rssNew/gundemRss.xml"},
    {"name": "Cumhuriyet", "url": "https://www.cumhuriyet.com.tr/rss/son_dakika"},
    {"name": "BBC Türkçe", "url": "https://feeds.bbci.co.uk/turkce/rss.xml"},
    {"name": "Euronews Türkçe", "url": "https://tr.euronews.com/rss"},
    {"name": "Haber7", "url": "https://i12.haber7.net/sondakika/news.xml"},
    {"name": "Yeni Şafak", "url": "https://www.yenisafak.com/rss"},
    {"name": "Daily Sabah", "url": "https://www.dailysabah.com/rss"},
    {"name": "Hürriyet Daily News", "url": "https://www.hurriyetdailynews.com/rss"},
    {"name": "T24", "url": "https://t24.com.tr/rss"},
    {"name": "Medyascope", "url": "https://medyascope.tv/feed/"},
    {"name": "BirGün", "url": "https://www.birgun.net/rss"},
    {"name": "Evrensel", "url": "https://www.evrensel.net/rss"},
    {"name": "Gazete Duvar", "url": "https://www.gazeteduvar.com.tr/rss"},
    {"name": "Diken", "url": "https://www.diken.com.tr/feed/"},
    {"name": "OdaTV", "url": "https://www.odatv.com/rss"},
    {"name": "Posta", "url": "https://www.posta.com.tr/rss"},
    {"name": "Takvim", "url": "https://www.takvim.com.tr/Rss"},
    {"name": "Karar", "url": "https://www.karar.com/rss"},
    {"name": "Türkiye Gazetesi", "url": "https://www.turkiyegazetesi.com.tr/rss"},
    {"name": "Akşam", "url": "https://www.aksam.com.tr/rss"},
    {"name": "Star", "url": "https://www.star.com.tr/rss"},
    {"name": "Aydınlık", "url": "https://www.aydinlik.com.tr/rss"},
    {"name": "Halk TV", "url": "https://halktv.com.tr/rss"},
    {"name": "Tele1", "url": "https://tele1.com.tr/feed/"},
    {"name": "KRT TV", "url": "https://krt.tv.tr/rss"},
    {"name": "A Haber", "url": "https://www.ahaber.com.tr/rss"},
    {"name": "İHA", "url": "https://www.iha.com.tr/rss"},
    {"name": "Sputnik Türkçe", "url": "https://tr.sputniknews.com/feed.xml"},
    {"name": "DW Türkçe", "url": "https://rss.dw.com/xml/rss_tr"},
    {"name": "VOA Türkçe", "url": "https://www.voaturkce.com/z/2956"},
    {"name": "Al Jazeera Türkçe", "url": "https://www.aljazeera.com.tr/rss/"},
    {"name": "Fotomac", "url": "https://www.fotomac.com.tr/rss"},
    {"name": "Fanatik", "url": "https://www.fanatik.com.tr/rss"},
    {"name": "Milliyet Spor", "url": "https://www.milliyet.com.tr/rss/rssNew/sporRss.xml"},
    {"name": "Hürriyet Spor", "url": "https://www.hurriyet.com.tr/rss/spor"},
    {"name": "Sözcü Spor", "url": "https://www.sozcu.com.tr/rss/spor"},
    {"name": "Habertürk Ekonomi", "url": "https://www.haberturk.com/rss/ekonomi"},
    {"name": "Sabah Ekonomi", "url": "https://www.sabah.com.tr/rss/ekonomi.xml"},
    {"name": "Cumhuriyet Ekonomi", "url": "https://www.cumhuriyet.com.tr/rss/ekonomi"},
    {"name": "Yetkin Report", "url": "https://yetkinreport.com/en/category/politics/feed/"},
    {"name": "National Turk", "url": "https://www.nationalturk.com/en/feed"},
    {"name": "A News", "url": "https://www.anews.com.tr/rss-feed"},
    {"name": "Insight Turkey", "url": "https://www.insightturkey.com/services/rss.xml"},
    {"name": "Duvar English", "url": "https://www.duvarenglish.com/export/rss"},
    {"name": "Türkiye Gazetesi Politika", "url": "https://www.turkiyegazetesi.com.tr/politika/rss"},
    {"name": "Euronews Turkish Politics", "url": "https://www.euronews.com/tag/turkish-politics/rss"},
    {"name": "Haberler.com", "url": "https://rss.haberler.com/rss.asp"},
    {"name": "MFA Türkiye", "url": "https://www.mfa.gov.tr/rss.en.mfa"},
    {"name": "Yenisaafak English", "url": "https://en.yenisafak.com/rss-list"},
    {"name": "Property Turkey", "url": "https://www.propertyturkey.com/blog-turkey/rss.xml"},
    {"name": "One Nation Travel", "url": "https://www.onenationtravel.com/blog/rss.xml"},
    {"name": "Turkish Foodie", "url": "https://www.turkishfoodie.com/feed"},
    {"name": "Fethiye Times", "url": "https://www.fethiyetimes.com/feed"},
    {"name": "Yabangee", "url": "https://yabangee.com/feed"},
    {"name": "CEE Legal Matters Turkey", "url": "https://ceelegalmatters.com/turkey/feed"},
    {"name": "Turkish Law Blog", "url": "https://turkishlawblog.com/feed"},
    {"name": "Doing Business in Turkey", "url": "https://www.doingbusinessinturkey.com/feed"},
    {"name": "Gaming in Turkey", "url": "https://gaminginturkey.com/en/feed"},
    {"name": "Fluent in Turkish", "url": "https://fluentinturkish.com/feed"},
    {"name": "HandsOnTurkish", "url": "https://turkishonline.eu/blog/feed"},
    {"name": "Ozlem's Turkish Table", "url": "https://ozlemsturkishtable.com/feed"},
    {"name": "Turkey's For Life", "url": "https://www.turkeysforlife.com/feeds/posts/default"},
    {"name": "Jane in Mersin", "url": "https://janeyinmersin.com/feed"},
    {"name": "Almost Turkish Recipes", "url": "https://almostturkishrecipes.com/feed"},
]

WINDOW_HOURS = 12
MAX_ITEMS = 300


def _parse_entry_datetime(entry: Any) -> Optional[datetime]:
    time_struct = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
    if time_struct is None:
        return None
    dt_naive = datetime(*time_struct[:6])
    return dt_naive.replace(tzinfo=timezone.utc)


def translate_text(text: str) -> str:
    """Translate using MyMemory API directly via HTTP requests."""
    if not text.strip():
        return text
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": "tr|he"}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if data.get("responseStatus") == 200:
            translated = data["responseData"]["translatedText"]
            if translated:
                return translated
    except Exception as e:
        logger.warning("Translation error: %s", e)
    return text


def parse_and_fetch():
    logger.info("Starting feed collection from %d feeds...", len(RSS_FEEDS))
    cutoff = datetime.now(timezone.utc) - timedelta(hours=WINDOW_HOURS)

    raw_entries: List[Dict[str, Any]] = []
    seen_links = set()

    for feed in RSS_FEEDS:
        name = feed["name"]
        url = feed["url"]
        try:
            parsed = feedparser.parse(url)
            for entry in parsed.entries:
                title = getattr(entry, "title", "").strip()
                link = getattr(entry, "link", "").strip()
                if not title or not link or link in seen_links:
                    continue

                pub_date = _parse_entry_datetime(entry)
                if pub_date and pub_date < cutoff:
                    continue

                seen_links.add(link)
                raw_entries.append(
                    {
                        "source": name,
                        "title_tr": title,
                        "link": link,
                        "timestamp": pub_date.timestamp() if pub_date else datetime.now(timezone.utc).timestamp(),
                        "fetched_at": datetime.now(timezone.utc).isoformat(),
                    }
                )
        except Exception as exc:
            logger.warning("Error fetching %s (%s): %s", name, url, exc)

    raw_entries.sort(key=lambda x: x["timestamp"], reverse=True)
    raw_entries = raw_entries[:MAX_ITEMS]

    logger.info("Translating %d titles to Hebrew...", len(raw_entries))
    all_items = []
    for item in raw_entries:
        title_tr = item["title_tr"]
        title_he = translate_text(title_tr)

        all_items.append(
            {
                "source": item["source"],
                "title_tr": title_tr,
                "title_he": title_he,
                "link": item["link"],
                "fetched_at": item["fetched_at"],
            }
        )

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    logger.info("Successfully exported %d news items to news.json", len(all_items))


if __name__ == "__main__":
    parse_and_fetch()
