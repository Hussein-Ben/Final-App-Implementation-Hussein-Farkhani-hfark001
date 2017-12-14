# This script is run on the mongoDB shell

var index = db.users.find( { type: 2 } ); # the "type 2" is just casting, type 2 means String, type 1 means double etc.

   printjson(index);


