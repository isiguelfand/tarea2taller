
from flask import Flask, jsonify, request, Response #, url_for, redirect, request
from flask_pymongo import PyMongo
from base64 import b64encode
from bson import json_util
from bson.objectid import ObjectId
#from flask_restful import Api, Resource
app = Flask(__name__)
nombre="mongodb+srv://user:"+"tallerintegracion"+"@cluster0.eikb3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#app.config["MONGO_URI"] = "mongodb://localhost/tarea"
app.config["MONGO_URI"] = nombre
mongo=PyMongo(app)

@app.route('/artists',methods=['POST'])
def create_artist():
    request.get_json(force=True)
    name=request.json["name"]
    age=request.json["age"]
    encoded = b64encode(name.encode()).decode('utf-8')
    if name and encoded and age:
        users=mongo.db.users.find_one({'id': encoded})
        if not users:
            albums= "https://tarea2artistas.herokuapp.com/artists/" + encoded + "/albums"
            tracks= "https://tarea2artistas.herokuapp.com/artists/" + encoded + "/tracks"
            url= "https://tarea2artistas.herokuapp.com/artists/" + encoded
            id = mongo.db.users.insert_one({'name': name, 'id': encoded,'albums': albums,'tracks': tracks,'url': url,'age': age})
            user=mongo.db.users.find_one({'id': encoded},{'_id': False})
            response=json_util.dumps(user)
            response=Response(response,"application/json")
            #message=jsonify({'message': response, 'Code': 201})
            response.status_code = 201
            return response
        else:
            return exists("artista ")
    else:
        return invalid()


@app.route('/artists/<ID>',methods=['GET'])
def show_artist(ID):
    user=mongo.db.users.find_one({'id': ID},{'_id': False})
    if not user:
        return not_found("Artista ")
    else:
        response=json_util.dumps(user)
        response=Response(response,"application/json")
        response.status_code =200
        return response


@app.route('/artists',methods=['GET'])
def show_artists():
    users=mongo.db.users.find({},{'_id': False})
    response=json_util.dumps(users)
    response=Response(response,"application/json")
    response.status_code =200
    return response





@app.route('/artists/<artist_ID>/albums',methods=['POST'])
def create_album(artist_ID):
    request.get_json(force=True)
    name=request.json["name"]
    genre=request.json["genre"]
    encoded = b64encode(name.encode()).decode('utf-8')
    user=mongo.db.users.find_one({'id': artist_ID},{'_id': False})
    if not user:
        return invalid_parent("Artista ")
    if name and encoded and genre:
        albums=mongo.db.albums.find_one({'id': encoded})
        if not albums:
            url= "https://tarea2artistas.herokuapp.com/" + "albums/" +encoded 
            tracks= "https://tarea2artistas.herokuapp.com/" + "albums/" +encoded +"/tracks"
            artist= "https://tarea2artistas.herokuapp.com/" + "artists/"+artist_ID 
            id = mongo.db.albums.insert_one({'name': name, 'id': encoded,'artist_id': artist_ID,'genre': genre,'url': url,'tracks': tracks})
            album=mongo.db.albums.find_one({'id': encoded},{'_id': False})
            response=json_util.dumps(album)
            response=Response(response,"application/json")
            #message=jsonify({'message': response, 'Code': 201})
            response.status_code = 201
            return response
        else:
            return exists("album ")
    else:
        return invalid()



@app.route('/albums/<ID>',methods=['GET'])
def show_album(ID):
    album=mongo.db.albums.find_one({'id': ID},{'_id': False})
    if not album:
        return not_found("Album ")
    else:
        response=json_util.dumps(album)
        response=Response(response,"application/json")
        response.status_code =200
        return response


@app.route('/albums',methods=['GET'])
def show_albums():
    albums=mongo.db.albums.find({},{'_id': False})
    response=json_util.dumps(albums)
    response=Response(response,"application/json")
    response.status_code =200
    return response


@app.route('/artists/<artist_ID>/albums',methods=['GET'])
def show_albums_artist(artist_ID):
    user=mongo.db.users.find_one({'id': artist_ID},{'_id': False})
    if not user:
        return invalid_parent("Artista ")
    albums=mongo.db.albums.find({'artist_id': artist_ID},{'_id': False})
    response=json_util.dumps(albums)
    response=Response(response,"application/json")
    response.status_code =200
    return response

@app.route('/albums/<album_ID>/tracks',methods=['GET'])
def show_tracks_album(album_ID):
    album=mongo.db.albums.find_one({'id': album_ID},{'_id': False})
    if not album:
        return invalid_parent("Album ")
    tracks=mongo.db.tracks.find({'artist_id': album_ID},{'_id': False})
    response=json_util.dumps(tracks)
    response=Response(response,"application/json")
    response.status_code =200
    return response


@app.route('/albums/<album_ID>/tracks',methods=['POST'])
def create_track(album_ID):
    request.get_json(force=True)
    name=request.json["name"]
    duration=request.json["duration"]
    encoded = b64encode(name.encode()).decode('utf-8')
    album=mongo.db.albums.find_one({'id': album_ID},{'_id': False})
    if not album:
        return invalid_parent("Album")
    if name and duration and encoded and album:
        artist_ID=album["artist_id"]
        tracks=mongo.db.albums.find_one({'id': encoded})
        if not tracks:
            url= "https://tarea2artistas.herokuapp.com/" + "tracks/"+ encoded 
            album= "https://tarea2artistas.herokuapp.com/albums"+ album_ID
            artist= "https://tarea2artistas.herokuapp.com/artists/"+ artist_ID 
            id = mongo.db.tracks.insert_one({'name': name, 'id': encoded,'artist': artist,'duration': duration,'url': url,'album_id': album_ID,'times_played': 0})
            track=mongo.db.tracks.find_one({'id': encoded},{'_id': False})
            response=json_util.dumps(track)
            response=Response(response,"application/json")
            #message=jsonify({'message': response, 'Code': 201})
            response.status_code = 201
            return response
        else:
            return exists("canción ")
    else:
        return invalid()


@app.route('/tracks/<ID>',methods=['GET'])
def show_track(ID):
    track=mongo.db.tracks.find_one({'id': ID},{'_id': False})
    if not track:
        return not_found("Canción ")
    else:
        response=json_util.dumps(track)
        response=Response(response,"application/json")
        response.status_code =200
        return response


@app.route('/tracks',methods=['GET'])
def show_tracks():
    tracks=mongo.db.tracks.find({},{'_id': False})
    response=json_util.dumps(tracks)
    response=Response(response,"application/json")
    response.status_code =200
    return response


@app.route('/artists/<artist_ID>/tracks',methods=['GET'])
def show_tracks_artist(artist_ID):
    user=mongo.db.users.find_one({'id': artist_ID},{'_id': False})
    if not user:
        return invalid_parent("Artista ")
    tracks=mongo.db.tracks.find({'artist_id': artist_ID},{'_id': False})
    response=json_util.dumps(tracks)
    response=Response(response,"application/json")
    response.status_code =200
    return response


@app.route('/tracks/<ID>/play',methods=['PUT'])
def play_track(ID):
    #request.get_json(force=True)
    track=mongo.db.tracks.find_one({'id': ID},{'_id': False})
    if not track:
        return not_found("Canción ")
    else:
        mongo.db.tracks.update({'id': ID}, { "$set": { "times_played": track["times_played"]+1 } })
        #track["times_played"]+=1
        #track.save()
        response=Response("canción reproducida","application/json")
        response.status_code =200
        return response

@app.route('/artists/<artist_ID>/tracks/play',methods=['PUT'])
def play_track_artist(artist_ID):
    request.get_json(force=True)
    user=mongo.db.users.find_one({'id': artist_ID},{'_id': False})
    if not user:
        return invalid_parent("Artista ")
    else:
        tracks=mongo.db.tracks.find({'artist_id': artist_ID},{'_id': False})
        for x in tracks: 
            mongo.db.tracks.update({'id': ID}, { "$set": { "times_played": track["times_played"]+1 } })
        response=Response("todas las canciones del artista fueron reproducidas","application/json")
        response.status_code =200
        return response

@app.route('/albums/<album_ID>/tracks/play',methods=['PUT'])
def play_track_album(album_ID):
    album=mongo.db.albums.find_one({'id': album_ID},{'_id': False})
    if not album:
        return invalid_parent("Album ")
    else:
        tracks=mongo.db.tracks.find({'artist_id': album_ID},{'_id': False})
        for x in tracks: 
            mongo.db.tracks.update({'id': ID}, { "$set": { "times_played": track["times_played"]+1 } })
        response=Response("canciones del álbum reproducidas","application/json")
        response.status_code =200
        return response



#@app.errorhandler(422)
def invalid_parent(parent,error=None):
    message=jsonify({'message': parent + ' no existe'})
    message.status_code =422
    return message



#@app.errorhandler(400)
def invalid(error=None):
    message=jsonify({'message': 'input inválido'})
    message.status_code =400
    return message

#@app.errorhandler(409)
def exists(model,error=None):
    message=jsonify({'message': model + 'ya existe'})
    message.status_code =409
    return message

#@app.errorhandler(404)
def not_found(model,error=None):
    message=jsonify({'message': model + 'no encontrado'})
    message.status_code =404
    return message

@app.errorhandler(404)
def error(model,error=None):
    message=jsonify({'message': 'method not allowed'})
    message.status_code =405
    return message


if __name__ == "__main__":
    app.run(debug=True)