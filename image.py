import MySQLdb
import distance
from PIL import Image
import imagehash

"""
Insert info into DB:
insert_image(aHash, bHash, pHash, location)
insert_tage(tag, pHash)

Subtract info from DB:
// No input and the output is a list of aHash
find_aHash()

// Input is one aHash value, the output is a list of bHash
find_bHash(aHash)   

// Input is one aHash value, the output is a list of pHash and location
find_pHash_a(aHash)

// Input is one bHash value, the output is a list of pHash and location
find_pHash_b(bHash)

// Input is a tag, the output is a list of location
get_location_by_tag(tag)

// Input is a string tag, the output is a list of string
auto_complete(tag)

"""


def hamming(ahash,phash):
	"""return the 10 most similar pics based on the hamming"""
	result = find_aHash();
	dist_a = 9
	dist_b = 16
	ahash_db = 0
	bhash_db = 0
	phash = str(convert_hex_to_bin(phash))
	for i in result:
		if distance.hamming(i, ahash) < dist_a:
			dist_a = distance.hamming(i,ahash)
			ahash_db = i			
	result_p  = find_pHash_a(ahash_db)
	print result_p
	resu =[]
	for x in result_p:
		y=list(x)
		y[0] = str(convert_hex_to_bin(y[0]))
		y.append(distance.hamming(phash,y[0]))
		resu.append(y)
	resu = sorted(resu,key=lambda x: x[2])
	if len(resu) <= 10:
		return resu
	else:
		return resu[0:10]

def get_format(result):
	x = []
	for item in result:
		x.append({'phash':item[0],'loc':item[1],'hamming':item[2]})
	return x

def pic_exist(phash):
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )
        cursor = cnx.cursor()
        # find all aHash values
        query_pic_exist = ("SELECT * FROM image WHERE phash = '%s'"%(phash))
        cursor.execute(query_pic_exist)
        result = cursor.fetchall()
    except Error as e:
        print e
    finally:
        cursor.close()
        cnx.close()
        if result:
           return True
        else:
           return False

def tag_exist(tag,phash):
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )
        cursor = cnx.cursor()
        # find all aHash values
        query_pic_exist = ("SELECT * FROM image WHERE phash = '%s'"%(phash))
        cursor.execute(query_pic_exist)
        result = cursor.fetchall()
        print result
    except Error as e:
        print e
    finally:
        cursor.close()
        cnx.close()
        print result
        if result:
           return True
        else:
           return False


def cal_hash_val(file_path):
	l = [3,4,16]
	hash_val = []
	for i in l:
		a = imagehash.phash(Image.open(file_path),i)
		a = str(a)
		if i != 16:
			a = bin(int(a,16))[2:].zfill(i**2)
		hash_val.append(str(a))
	return hash_val

def convert_hex_to_bin(hex):
	return bin(int(hex,16))[2:].zfill(16**2)


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
        ret = []
        for i in result:
            ret.append(i[0])
    
    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()
        return ret

def find_bHash(aHash): 
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )
        cursor = cnx.cursor()
        # find the bHash which is belongs to specific aHash
        cursor.execute("SELECT DISTINCT bHash FROM image WHERE aHash = '%s'"% (aHash))
        result = cursor.fetchall() 
        ret = []
        for i in result:
            ret.append(i[0])

    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()
        return ret

def find_pHash_a(aHash):
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )
        cursor = cnx.cursor()
        # find the pHash which is belongs to the specific aHash
        cursor.execute("SELECT pHash, location FROM image WHERE aHash = '%s'"% (aHash))
        result = cursor.fetchall()
        ret = []
        for i in result:
            ret.append(i)

    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()
        return ret


def find_pHash_b(bHash):
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )
        cursor = cnx.cursor()
        # find the pHash which is belongs to the specific aHash
        cursor.execute("SELECT pHash, location FROM image WHERE bHash = '%s'"% (bHash))
        result = cursor.fetchall()
        ret = []
        for i in result:
            ret.append(i)

    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()
        return ret

def get_location_by_tag(tag):
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )
        cursor = cnx.cursor()
        # find the pHash which is belongs to the specific aHash
        cursor.execute("SELECT location FROM image WHERE pHash IN (SELECT pHash FROM tags WHERE tag = '%s')"% (tag))
        result = cursor.fetchall()
        ret = []
        for i in result:
            ret.append(i[0])

    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()
        return ret

def auto_complete():
    try:   
        cnx = MySQLdb.connect(
            user = 'dbmanager',
            passwd = '123456',
            host = 'localhost',
            db = 'imagesearch'
        )
        cursor = cnx.cursor()
        # find the pHash which is belongs to the specific aHash
        cursor.execute("SELECT DISTINCT tag FROM tags ")
        result = cursor.fetchall()
        ret = []
        for i in result:
            ret.append(i[0])

    except Error as e:
        print e

    finally:
        cursor.close()
        cnx.close()
        return ret
