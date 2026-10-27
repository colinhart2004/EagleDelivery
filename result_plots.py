import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import argparse
from pathlib import Path

#map 0-2 trainings to different marker shapes in final plot
dataset_configs = {
    "training 0" : {"file": "training_seed0.csv", "marker": "o"},
    "training 1" : {"file": "training_seed1.csv", "marker": "^"},
    "training 2" : {"file": "training_seed2.csv", "marker": "s"},
}

#true or false colors for success
success_colors = {
    True: "#05ad02",
    False: "#d40000",
}

fig,ax = plt.subplots(figsize=(9,6))

def main():
    #get folder argument
    parser = argparse.ArgumentParser(description="Generate a plot from results of running the training model")
    parser.add_argument("folder")
    parser.add_argument("title")
    args = parser.parse_args()
    folder = Path(args.folder)


    for _, config in dataset_configs.items():
        df = pd.read_csv(folder / config["file"])

        if df.empty:
            parser.error("unable to read" + config["file"])

        #get y as number of steps
        #get x as episode number
        y = df.iloc[:, 1]
        x = df.iloc[:, 0]
        #get successes as the boolean row 3
        success = df.iloc[:, 3].astype(bool)

        #if true, green, if false, red
        point_colors = success.map(success_colors)

        ax.scatter(
            x,
            y,
            c=point_colors,
            marker=config["marker"],
            s=10,
            alpha=0.7,
            edgecolors="black",
            linewidths=0.3,
        )

    #legend 1, training 0-2
    shape_handles = [
        mlines.Line2D(
            [], [],
            color="#555555",
            marker=cfg["marker"],
            linestyle="None",
            markersize=8,
            label=name,
        )
        for name, cfg in dataset_configs.items()
    ]
    legend_shapes = ax.legend(
        handles=shape_handles,
        title="Training Markers",
        #move legend to the top right of the plot window
        bbox_to_anchor=(1.02, 1.0),
        loc="upper left",
        borderaxespad=0,
    )

    #attach legend 1 so the next legend call does not overwrite it
    ax.add_artist(legend_shapes)

    #legend 2, success colors
    color_handles = [
        mlines.Line2D(
            [], [],
            color=col,
            marker="o",
            linestyle="None",
            markersize=8,
            label=str(state),
        )
        for state, col in success_colors.items()
    ]
    legend_colors = ax.legend(
        handles=color_handles,
        title="Was Successful",
        bbox_to_anchor=(1.02, 0.65),
        loc="upper left",
        borderaxespad=0,
    )

    #set x and y label + title
    ax.set_xlabel("Episode")
    ax.set_ylabel("Number of Steps")
    ax.set_title(args.title + " Training Accuracies Over Episode Numbers")
    #add grid
    ax.grid(True, linestyle="--", alpha=0.4)

    #clean up spacing
    plt.tight_layout()
    
    plt.show()

if __name__ == "__main__":
    main()