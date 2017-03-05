def rssi2dist(rssi):
    dist=0
    if rssi>=-40:dist=20
    elif rssi>=-50:dist=26
    elif rssi>=-60:dist=40
    elif rssi>=-70:dist=100
    else:dist=120
    return dist