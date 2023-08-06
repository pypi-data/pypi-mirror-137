Lightweight a movie and TV series data parser like title, alternate title, release date, runtime, age rating and episode titles for TV series from imdb.com and kinopoisk.ru without using third-party packages. Wget will be used for the kinopoisk parser, so Linux like only.

Install:

    pip install imkin

Examples:

    import imkin
    
    film = imkin.new('https://www.imdb.com/title/tt0068646/')
    
    print(film)
    
    print(film.title)
    
    print(film.alternate)
    
    print(film.year)
    
    print(film.time)
    
    print(film.age)
    
    print(film.isfilm)
    
    print(film.url)
    
    
    film = imkin.new('https://www.imdb.com/title/tt2356777/')
    
    print(film.title)
    
    titles = imkin.gettitles(film.url)
    
    print(titles[1][1])
    
    
    result = imkin.search('Fargo')
    
    print(result)
