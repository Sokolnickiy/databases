DROP_COUNTRY = """
    DROP TABLE IF EXISTS country CASCADE;
"""

DROP_CATEGORY = """
    DROP TABLE IF EXISTS category CASCADE;
"""

DROP_WEBSITE = """
    DROP TABLE IF EXISTS website CASCADE;
"""


CREATE_TABLE_COUNTRY = """
    CREATE TABLE country(
        "id" int GENERATED ALWAYS AS IDENTITY,
        "country_name" VARCHAR(50),
        PRIMARY KEY ("id")
    );
"""

CREATE_TABLE_CATEGORY = """
    CREATE TABLE category(
        "id" int GENERATED ALWAYS AS IDENTITY,
        "category_type" text,
        PRIMARY KEY ("id")
    );
"""

CREATE_TABLE_WEBSITE = """
    CREATE TABLE website (
        "id" int GENERATED ALWAYS AS IDENTITY,
        "principal_country" int REFERENCES country("id"),
        "site" VARCHAR(50),
        "category_id" int REFERENCES category("id"),
        "domain_name" VARCHAR(50),
        PRIMARY KEY ("id")
    );
"""


POPULATE_COUNTRY = """
    INSERT INTO country("country_name") VALUES
        ('United States'),
        ('China'),
        ('Russia'),
        ('Czech Republic');
    
"""

POPULATE_CATEGORY = """
    INSERT INTO category("category_type") VALUES
        ('Computers Electronics and Technology > Search Engines'),
        ('Arts & Entertainment > Streaming & Online TV'),
        ('Computers Electronics and Technology > Social Media Networks'),
        ('Reference Materials > Dictionaries and Encyclopedias'),
        ('News & Media Publishers'),
        ('Adult');
"""

POPULATE_WEBSITE = """
    INSERT INTO website(
        "principal_country",
        "site",
        "category_id",
        "domain_name"
    ) VALUES
        (1, 'Google Search', 1, 'google.com'),
        (1, 'YouTube', 2, 'youtube.com'),
        (1, 'Facebook', 3, 'facebook.com'),
        (1, 'Twitter', 3, 'twitter.com'),
        (1, 'Instagram', 3, 'instagram.com'),
        (2, 'Baidu', 1, 'baidu.com'),
        (1, 'Wikipedia', 4, 'wikipedia.org'),
        (3, 'Yandex', 1, 'yandex.ru'),
        (1, 'Yahoo', 5, 'yahoo.com'),
        (4, 'xVideos', 6, 'xvideos.com'),
        (1, 'WhatsApp', 3, 'whatsapp.com');
"""

CATEGORY_TYPE_POPULARITY = """
    SELECT count(*), c.category_type FROM website
    JOIN category c ON c.id = website.category_id
    GROUP BY c.category_type;
"""

COUNTRY_IMPACT = """
    SELECT count(*), c.country_name FROM website
    JOIN country c on c.id = website.principal_country
    GROUP BY c.country_name;
"""

COUNTRY_MOST_POPULAR_CATEGORY = """
    SELECT DISTINCT ON(country_name) * from (
        SELECT  count(*) as category_count, cou.country_name, cat.category_type FROM website
        JOIN category cat ON cat.id = website.category_id
        JOIN country cou ON cou.id = website.principal_country
        GROUP BY cou.country_name, cat.category_type
        ) q
    ORDER BY country_name, category_count DESC;
"""