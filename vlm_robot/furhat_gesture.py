
def tilt_head(furhat):
    furhat.gesture(body={
        "frames": [
            {
            "time": [
                0.17, 1.0, 6.0
            ],
            "params": {
                # "NECK_ROLL": 25.0,
                "NECK_ROLL": 0.0,

                ## NOTE: PAN to the left or right. where positiive is furhat's left
                # "NECK_PAN": -12.0,
                "NECK_PAN": 12.0,
                # "NECK_TILT": -25.0
                "NECK_TILT": 0.0
            }
            },
            {
                "time": [
                    7.0
                ],
                "params": { 
                    "reset": True
                }
            }
        ],
        "name": "Cool Thing",
        "class": "furhatos.gestures.Gesture"
        }
    )