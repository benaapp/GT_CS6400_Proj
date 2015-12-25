import MySQLdb

"""
Insert info into DB:
insert_image(aHash, bHash, pHash, location)
insert_tage(tag, pHash)

Subtract info from DB:
// No input and the output is a list of aHash
find_aHash()

// Input is one aHash value, the output is a list of bHash
find_bHash(aHash)   

// Input is one aHash value, the output is a list of pHash
find_pHash_a(aHash)

// Input is one bHash value, the output is a list of pHash
find_pHash_b(bHash)

// Input is a list of pHash, the output is a list of location 
get_location_by_pHash(pHash)

// Input is a tag, the output is a list of location
get_location_by_tag(tag)

// Input is a string tag, the output is a list of string
auto_complete(tag)

"""

def insert_image(aHash, bHash, pHash, location): 
    try:   
        cnx = MySQLdb.connect(
                user = 'dbmanager',
                passwd = '123456',
                host = 'localhost',
                db = 'imagesearch'
            )
        cursor = cnx.cursor()
        # find all aHash values
        query_insert_image = ("INSERT INTO image "
                            "(aHash, bHash, pHash, location) "
                            "VALUES (%s, %s, %s, %s)"
                            )
        add_value = (str(aHash), str(bHash), str(pHash), str(location))
        cursor.execute(query_insert_image, add_value)
        cnx.commit()
    
    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()


def insert_tags(tag, pHash): 
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )
        cursor = cnx.cursor()
        # find all aHash values
        query_insert_tag = ("INSERT INTO tags "
                            "(tag, pHash) "
                            "VALUES (%s, %s)"
                            )
        add_value = (str(tag), str(pHash))
        cursor.execute(query_insert_tag, add_value)
        cnx.commit()
    
    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()


def find_aHash():
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )
        cursor = cnx.cursor()
        # find all aHash values
        query_find_aHash = ("SELECT DISTINCT aHash FROM image")
        cursor.execute(query_find_aHash)
        result = cursor.fetchall()
        print result
    
    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()
        return result

def find_bHash(aHash): 
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )

        # find the bHash which is belongs to specific aHash
        query_find_bHash = ("SELECT DISTINCT bHash FROM image WHERE aHash = %s")
        cursor.execute(query_find_bHash, aHash)
        result = cursor.fetchall()
    
    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()
        return result

def find_pHash_a(aHash):
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )

        # find the pHash which is belongs to the specific aHash
        query_find_pHash_a = ("SELECT pHash FROM image WHERE aHash = %s")
        cursor.execute(query_find_pHash_a, aHash)
        result = cursor.fetchall()
    
    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()
        return result



# find the pHash which is belongs to the specific bHash


if __name__ == '__main__':
    aHash = '001001101'
    bHash = '1001011101000101'
    pHash = '8d699c69c998669c63b2694e339ec6b26146993113e7636e9c3339c3e33c1ce6'
    location = 'http://location_1'
    tag = "black"
    #insert_image(aHash, bHash, pHash, location)
    #insert_tags(tag, pHash)
    result = find_aHash()
    print result
