import matplotlib.pyplot as plt

landmarks  = {
    "nose": [0.26625069975852966, 0.33803537487983704],
    "left_eye": [0.2560405135154724, 0.3242892324924469],
    "right_eye": [0.257402628660202, 0.32049259543418884],
    "left_ear": [0.25878646969795227, 0.31644532084465027],
    "right_ear": [0.252015084028244, 0.3273991346359253],
    "left_shoulder": [0.2506130337715149, 0.32605689764022827],
    "right_shoulder": [0.24929487705230713, 0.3246411085128784],
    "left_elbow": [0.2674368917942047, 0.2919197380542755],
    "right_elbow": [0.2534945607185364, 0.3076714873313904],
    "left_wrist": [0.2832384407520294, 0.3295455276966095],
    "right_wrist": [0.27710774540901184, 0.335440993309021],
    "left_pinky": [0.3594854474067688, 0.24842919409275055],
    "right_pinky": [0.28572461009025574, 0.31927749514579773],
    "left_index": [0.43833377957344055, 0.15734857320785522],
    "right_index": [0.22468726336956024, 0.382561594247818],
    "left_thumb": [0.5317646265029907, 0.19259819388389587],
    "right_thumb": [0.1710633635520935, 0.3684663772583008],
    "left_hip": [0.5606578588485718, 0.1949099600315094],
    "right_hip": [0.14658485352993011, 0.36216527223587036],
    "left_knee": [0.5578015446662903, 0.2075834572315216],
    "right_knee": [0.15180519223213196, 0.3570180833339691],
    "left_heel": [0.5478498935699463, 0.21000444889068604],
    "right_heel": [0.16408291459083557, 0.35783472657203674],
    "left_foot_index": [0.5201914310455322, 0.4207984209060669],
    "right_foot_index": [0.49776703119277954, 0.44816023111343384],
    "left_ankle": [0.35592666268348694, 0.5346580743789673],
    "right_ankle": [0.6166242361068726, 0.5757725238800049],
    "left_foot_tip": [0.5107901692390442, 0.6443974375724792],
    "right_foot_tip": [0.7800197601318359, 0.6710343360900879],
    "left_foot_outside": [0.552850604057312, 0.6498035788536072],
    "right_foot_outside": [0.812722384929657, 0.6669078469276428]
}


x_coords = [landmark[0] for landmark in landmarks.values()]
y_coords = [landmark[1] for landmark in landmarks.values()]

plt.figure(figsize=(8, 8))
plt.scatter(x_coords, y_coords, color='blue')

for label, (x, y) in landmarks.items():
    plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('2D Pose Landmarks (X-Y plane)')

plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()
