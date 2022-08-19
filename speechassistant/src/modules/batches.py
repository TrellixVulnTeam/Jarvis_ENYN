
def batchGen(batch):
    """
    With the batchGen-function you can generate fuzzed compare-strings
    with the help of a easy syntax:
        "Wann [fährt|kommt] [der|die|das] nächst[e,er,es] [Bahn|Zug]"
    is compiled to a list of sentences, each of them combining the words
    in the brackets in all different combinations.
    This list can then fox example be used by the batchMatch-function to
    detect special sentences.
    """
    outlist = []
    ct = 0
    while len(batch) > 0:
        piece = batch.pop()
        if "[" not in piece and "]" not in piece:
            outlist.append(piece)
        else:
            frontpiece = piece.split("]")[0]
            inpiece = frontpiece.split("[")[1]
            inoptns = inpiece.split("|")
            for optn in inoptns:
                rebuild = frontpiece.split("[")[0] + optn
                rebuild += "]".join(piece.split("]")[1:])
                batch.append(rebuild)
    return outlist


def batchMatch(batch, match):
    if isinstance(batch, str):
        batch = [batch]
    for piece in batchGen(batch):
        if piece.lower() in match.lower():
            return True
    return False
