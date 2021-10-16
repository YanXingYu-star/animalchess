import json
import piece


def create_piece():
    with open("piece.json", "r",encoding="utf-8") as f:
        data = json.load(f)    
    for i in data['piece']:
        a=piece.Piece(i["name"],i["team"],*eval(i["pos"]))
        print("{}'s pos = {}".format(a.name,a.get_pos()))

create_piece()
print(piece.Piece.get_all_pieces())
    
