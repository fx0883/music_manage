-- 删除所有表数据
-- 注意：删除顺序要考虑外键约束

-- 1. 先删除依赖表的数据
DELETE FROM chinese_annotation;
DELETE FROM chinese_appreciation;
DELETE FROM chinese_interpretation;
DELETE FROM chinese_poemgenrerelation;

-- 2. 再删除主表数据
DELETE FROM chinese_poem;
DELETE FROM chinese_author;
DELETE FROM chinese_poemtype;
DELETE FROM chinese_poemgenre;
DELETE FROM chinese_language;

-- 查询所有表数据
-- 1. 查询基础表数据
SELECT * FROM chinese_language;
SELECT * FROM chinese_poemtype;
SELECT * FROM chinese_poemgenre;
SELECT * FROM chinese_author;

-- 2. 查询诗词表数据
SELECT 
    p.id,
    p.title,
    p.title_pinyin,
    a.name as author_name,
    pt.name as poem_type,
    pg.name as poem_genre,
    p.content,
    p.pinyin,
    p.difficulty
FROM chinese_poem p
LEFT JOIN chinese_author a ON p.author_id = a.id
LEFT JOIN chinese_poemtype pt ON p.poem_type_id = pt.id
LEFT JOIN chinese_poemgenrerelation pgr ON p.id = pgr.poem_id
LEFT JOIN chinese_poemgenre pg ON pgr.genre_id = pg.id;

-- 3. 查询注释数据
SELECT 
    p.title,
    l.name as language,
    a.content
FROM chinese_annotation a
JOIN chinese_poem p ON a.poem_id = p.id
JOIN chinese_language l ON a.language_id = l.id;

-- 4. 查询赏析数据
SELECT 
    p.title,
    l.name as language,
    a.content
FROM chinese_appreciation a
JOIN chinese_poem p ON a.poem_id = p.id
JOIN chinese_language l ON a.language_id = l.id;

-- 5. 查询译文数据
SELECT 
    p.title,
    l.name as language,
    i.title_translation,
    i.content
FROM chinese_interpretation i
JOIN chinese_poem p ON i.poem_id = p.id
JOIN chinese_language l ON i.language_id = l.id;

-- 6. 统计数据
SELECT 'Languages' as table_name, COUNT(*) as count FROM chinese_language
UNION ALL
SELECT 'Poem Types', COUNT(*) FROM chinese_poemtype
UNION ALL
SELECT 'Poem Genres', COUNT(*) FROM chinese_poemgenre
UNION ALL
SELECT 'Authors', COUNT(*) FROM chinese_author
UNION ALL
SELECT 'Poems', COUNT(*) FROM chinese_poem
UNION ALL
SELECT 'Annotations', COUNT(*) FROM chinese_annotation
UNION ALL
SELECT 'Appreciations', COUNT(*) FROM chinese_appreciation
UNION ALL
SELECT 'Interpretations', COUNT(*) FROM chinese_interpretation; 