class Query:
    GRAPH = """
        MATCH (n)
        WHERE n:Interview OR n:Artist OR n:Theme
        OPTIONAL MATCH (n)-[r]->(m)
        WHERE m:Interview OR m:Artist OR m:Theme

        OPTIONAL MATCH (n:Interview)-[:CONTAINS]->(:Video)<-[ra:RESPONDS]-(a:Artist)

        OPTIONAL MATCH (n:Interview)-[:CONTAINS]->(:Video)<-[rq:HAS_ANSWERS]-(:Question)-[rt:IS_THEMED]->(theme:Theme)
        WITH n, collect(distinct rt) + collect(DISTINCT r) + collect(DISTINCT ra) AS relations, collect(DISTINCT theme) + collect( DISTINCT m) + collect( DISTINCT a) AS target
        return n, relations, target
        """


    INTERVIEWS_THEMES = """
        MATCH (theme:Theme)<-[:IS_THEMED]-(question:Question)<-[:ANSWERED]-(answer:Answer)<-[:CONTAINS]-(video:Video)
        WHERE elementId(video) = $video_id
        RETURN theme
        """

    INTERVIEWS_ARTISTS= """
        MATCH (v:Video)-[:CONTAINS]->(a:Answer)-[:ANSWERED_BY]->(artist:Artist)
        WHERE elementId(v) = $video_id
        RETURN DISTINCT artist
        """
    
    VIDEO_THEMES = """
        MATCH (theme:Theme)<-[:IS_THEMED]-(question:Question)-[:HAS_ANSWERS]->(video:Video)
        WHERE elementId(video) = $video_id
        RETURN theme
        """
    
    VIDEO_AUTHOR = """
        MATCH (author:Author)<-[:PUBLISHED_BY]-(interview:Interview)-[:CONTAINS]->(video:Video)
        WHERE elementId(video) = $video_id
        RETURN author
        """
    
    THEME_VIDEOS = """
        MATCH (theme:Theme)<-[:IS_THEMED]-(question:Question)-[:HAS_ANSWERS]->(video:Video)
        WHERE elementId(theme) = $theme_id
        RETURN video
        """
    
    ARTIST_VIDEOS = """
        MATCH (v:Video)<-[:RESPONDS]-(artist:Artist)
        WHERE elementId(artist) = $artist_id
        RETURN DISTINCT v
        """
    
    ARTIST_PREFERRED_THEMES = """
        MATCH (artist:Artist)-[:RESPONDS]->(a:Video)<-[:HAS_ANSWERS]-(q:Question)-[:IS_THEMED]->(t:Theme)
        WHERE elementId(artist) = $artist_id
        WITH t, COUNT(a) AS occurrences
        ORDER BY occurrences DESC
        LIMIT 1
        RETURN t, elementId(t), t.name
        """