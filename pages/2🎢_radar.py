from mplsoccer import Radar, FontManager
import matplotlib.pyplot as plt
import streamlit as st 
from langchain.llms import OpenAI

def plot_radar_comparison(player1_data, player2_data, params, low, high, lower_is_better=[]):
    """
    Plot a radar comparison chart of two football players using the mplsoccer package.

    Args:
        player1_data (list): Data values for Player 1.
        player2_data (list): Data values for Player 2.
        params (list): Parameter names of the statistics to show.
        low (list): Lower boundaries for the statistics.
        high (list): Upper boundaries for the statistics.
        lower_is_better (list): List of parameters where lower values are better.

    Returns:
        matplotlib.figure.Figure: The radar comparison chart.
    """
    # Create FontManager instances for fonts
    font_urls = [
        ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/SourceSerifPro-Regular.ttf',
         FontManager),
        ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/SourceSerifPro-ExtraLight.ttf',
         FontManager),
        ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/RubikMonoOne-Regular.ttf',
         FontManager),
        ('https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf',
         FontManager),
        ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf',
         FontManager)
    ]
    
    font_managers = [FontManager(url) for url, FontManager in font_urls]

    # Create Radar instance
    radar = Radar(params, low, high,
                  lower_is_better=lower_is_better,
                  round_int=[False] * len(params),
                  num_rings=4,
                  ring_width=1,
                  center_circle_radius=1)

    # Plot the radar
    fig, ax = radar.setup_axis()
    radar.draw_circles(ax=ax, facecolor='#ffb2b2', edgecolor='#fc5f5f')
    radar_output = radar.draw_radar_compare(player1_data, player2_data, ax=ax,
                                            kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6},
                                            kwargs_compare={'facecolor': '#d80499', 'alpha': 0.6})
    _, _, _, _ = radar_output
    radar.draw_range_labels(ax=ax, fontsize=15, fontproperties=font_managers[3].prop)
    radar.draw_param_labels(ax=ax, fontsize=15, fontproperties=font_managers[3].prop)
    title1_text = ax['title'].text(0.01, 0.65, player1_data[0], fontsize=25, color='#01c49d',
                                fontproperties=robotto_bold.prop, ha='left', va='center')
    title2_text = ax['title'].text(0.01, 0.25, player1_data[1], fontsize=20,
                                    fontproperties=robotto_thin.prop,
                                    ha='left', va='center', color='#01c49d')
    title3_text = ax['title'].text(0.99, 0.65, player2_data[0], fontsize=25,
                                    fontproperties=robotto_bold.prop,
                                    ha='right', va='center', color='#d80499')
    title4_text = ax['title'].text(0.99, 0.25, player2_data[1], fontsize=20,
                                    fontproperties=robotto_thin.prop,
                                    ha='right', va='center', color='#d80499')

    return fig


params = ["npxG", "Non-Penalty Goals", "xA", "Key Passes", "Through Balls",
          "Progressive Passes", "Shot-Creating Actions", "Goal-Creating Actions",
          "Dribbles Completed", "Pressure Regains", "Touches In Box", "Miscontrol"]
low =  [0.08, 0.0, 0.1, 1, 0.6,  4, 3, 0.3, 0.3, 2.0, 2, 0]
high = [0.37, 0.6, 0.6, 4, 1.2, 10, 8, 1.3, 1.5, 5.5, 5, 5]


bruno_values = [0.25, 0.45, 0.35, 2.5, 0.8, 6, 5, 0.9, 1.2, 4.0, 3.5, 2]
bruyne_values = [0.32, 0.55, 0.45, 3.0, 1.0, 7, 6, 1.0, 1.4, 4.5, 4.0, 3.8]



fig = plot_radar_comparison(bruno_values, bruyne_values, params, low, high, lower_is_better=['Miscontrol'])

st.pyplot(fig)