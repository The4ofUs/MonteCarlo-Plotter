import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

RADIUS = 1
DETECTOR_CENTER = (0, 0, 1)

PATH_TO_CSV = sys.argv[1]

data = pd.read_csv(PATH_TO_CSV)
total = data[["X", "Y", "Z"]]
detected = data.loc[data["State"] == "DETECTED", ["X", "Y", "Z"]]
detected_percentage = (detected.shape[0]/data.shape[0])*100
terminated = data.loc[data["State"] == "TERMINATED", ["X", "Y", "Z"]]
terminated_percentage = (terminated.shape[0]/data.shape[0])*100
escaped = data.loc[data["State"] == "ESCAPED", ["X", "Y", "Z"]]
escaped_percentage = (escaped.shape[0]/data.shape[0])*100
print("Results :\n\tDetected Percentage = {}%\n\tTerminated Percentage = {}%\n\tEscaped Percentage = {}%\n".format(detected_percentage, terminated_percentage, escaped_percentage))
fig = plt.figure(figsize=(plt.figaspect(.5)))
fig.canvas.set_window_title("Monte Carlo Simulation")
# 3D Plots
photons_ax = fig.add_subplot(231, projection='3d')
photons_ax.scatter(total['X'], total['Y'], total['Z'], c='b', marker='.')
photons_ax.set_title('Photons | {}'.format(total.shape[0]))
terminated_ax = fig.add_subplot(2, 3, 5, projection='3d')
terminated_ax.scatter(terminated['X'], terminated['Y'], terminated['Z'], c='red', marker='.')
terminated_ax.set_title('Terminated | {}'.format(terminated.shape[0]))
detected_ax = fig.add_subplot(2, 3, 2, projection='3d')
detected_ax.scatter(detected['X'], detected['Y'], detected['Z'], c='green', marker='.')
detected_ax.set_title('Detected | {}'.format(detected.shape[0]))
escaped_ax = fig.add_subplot(234, projection='3d')
escaped_ax.scatter(escaped['X'], escaped['Y'], escaped['Z'], c='black', marker='.')
escaped_ax.set_title('Escaped | {}'.format(escaped.shape[0]))
# Profile
fiberGenerator_ax = fig.add_subplot(2, 3, 3)
detected.plot.scatter(x="X", y="Y", alpha=0.5,
                      c='Green', ax=fiberGenerator_ax, marker='.').tick_params(axis='both', which='both', left=False,
                                                                               bottom=False,
                                                                               labelbottom=False, labelleft=False)
detector = plt.Circle((DETECTOR_CENTER[0], DETECTOR_CENTER[1]), RADIUS, color='black', fill=False, linestyle='dotted')
fiberGenerator_ax.add_artist(detector)
fiberGenerator_ax.set(xlim=(-RADIUS, RADIUS), ylim=(-RADIUS, RADIUS), xlabel="", ylabel="", frame_on=False)

# Distribution
data["Distances"] = (((detected["X"] - DETECTOR_CENTER[0]) ** 2) + ((detected["Y"] - DETECTOR_CENTER[1]) ** 2) + (
        (detected["Z"] - DETECTOR_CENTER[2]) ** 2)) ** 0.5
fiberGeneratorProfile_ax = fig.add_subplot(2, 3, 6)
distribution = data["Distances"] - data["Distances"].mean()
std = data['Distances'].std()
sns.set(style="white", palette="muted", color_codes=True)
sns.despine(left=True)
sns.distplot(distribution, hist=False, ax=fiberGeneratorProfile_ax, color='g', kde_kws={"shade": True})
fiberGeneratorProfile_ax.tick_params(axis='both', which='both', left=False, bottom=False, labelleft=False)
fiberGeneratorProfile_ax.set(xlim=(-3*std, 3*std))

plt.show()