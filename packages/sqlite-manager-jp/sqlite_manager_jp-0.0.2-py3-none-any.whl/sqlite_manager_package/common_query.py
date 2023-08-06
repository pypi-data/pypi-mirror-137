"""
common sqlite queries
"""

class CommonQuery:

    select_count_table = """
        SELECT count(name) FROM sqlite_master 
        WHERE type = 'table' AND name = (?) 
    """ 

    