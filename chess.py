# -*- coding: utf-8 -*-
"""
Personal Project:
    Investigating chess openings and strategy using data from the well
    known site lichess.

@author: Beckett Sanderson
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CHESS = "games.csv"

def understand(df):
    """
    A function to display info about a df in one line

    Parameters
    ----------
    df : data frame
        any data frame containing info to display.

    Returns
    -------
    None.

    """
    # prints out info about data frame
    print(df.head(), "\n")
    print(df.describe(), "\n")
    print(df.shape, "\n")
    
    
def read_csv(filename, headers = None):
    """
    Reads in a csv with pandas to create a data frame

    Parameters
    ----------
    filename : string
        the location of the file to read in data from.
    headers : list, optional
        the names for the headers of the columns.

    Returns
    -------
    df : data frame
        a data frame containing all the data from the csv.

    """
    df = pd.read_csv(filename)
    
    # sets column headers if there are none already
    if headers != None:
        
        df.columns = headers
    
    #understand(df)
    
    return df

def get_min(val1, val2):
    """
    Compare to values and return the smaller value

    Parameters
    ----------
    val1 : int
        one number to compare.
    val2 : int
        a second number to compare.

    Returns
    -------
    int
        the smaller of the two values.

    """
    if val1 >= val2:
        return val2
    
    else:
        return val1


def df_cleaning(df):
    """
    Cleans the data frame for various factors to make analysis easier

    Parameters
    ----------
    df : data frame
        df containing info on chess games.

    Returns
    -------
    df : data frame
        the same data frame cleaned of specific values.

    """
    # drops columns I'm not using for the analysis
    df = df.drop(["id", "created_at", "last_move_at", "increment_code", 
                  "white_id", "black_id", "moves"], axis = 1)
    
    # only use rated games for competitiveness factor
    df = df[df["rated"] == True]
    
    # opening moves has to be >= 2
    df = df[df["opening_ply"] >= 2]
    
    # create min_rating column
    df["min_rating"] = df.apply(lambda row: get_min(row["white_rating"], 
                                                    row["black_rating"]), 
                                axis = 1)
    
    # display the df to ensure I've done what I want to
    understand(df)
    
    return df


def by_rating(df, min_rating, max_rating, clean = False):
    """
    Splits a df into a smaller df based around the ratings of the players

    Parameters
    ----------
    df : data frame
        data frame containing info about chess games.
    min_rating : int
        the minimum rating of the range.
    max_rating : int
        the maximum rating of the range.
    clean : boolean
        whether or not to clear out large disrepancies.

    Returns
    -------
    new_df : data frame
        a smaller data frame containing only games with certain ratings.

    """
    # narrows down the df to only having games within the rating range
    new_df = df[df["min_rating"] > min_rating]
    new_df = new_df[new_df["min_rating"] <= max_rating]
    
    # checks whether to clear out the large disrepancies
    if clean:
        
        # remove overly large rating discrepancies
        new_df = new_df[abs(new_df["white_rating"] - 
                        new_df["black_rating"]) <= 400]
    
    return new_df


def split_openings(df):
    """
    Splits the data frame into a dictionary containing the different 
    openings and their corresponding data

    Parameters
    ----------
    df : data frame
        data frame containing data related to different chess games.

    Returns
    -------
    opening_dict : dictionary
        dictionary containing openings and data related to those openings.

    """
    opening_dict = {}
    
    # get list of each unique opening
    opening_names = df["opening_name"].unique()
    
    # loops through each unique opening
    for opening in opening_names:
        
        # initializes counter variables for each opening
        white_wins = 0
        black_wins = 0
        draws = 0
        game_counter = 0
        
        # loops through every row in the data frame
        for idx in df.index:
            
            # checks if the opening matches the line of the df
            if df["opening_name"][idx] == opening:
                
                # checks whether the winner was white, black or neither
                if df["winner"][idx] == "white":
                    
                    # adds to counter depending on winner
                    white_wins += 1
                    game_counter += 1
                    
                elif df["winner"][idx] == "black":
                    
                    black_wins += 1
                    game_counter += 1
                    
                else:
                    
                    draws += 1
                    game_counter += 1
        
        # adds opening to the dictionary with it's gathered data
        opening_dict[opening] = [white_wins, black_wins, draws, game_counter]
    
    return opening_dict


def graph_organization(title, xlabel, ylabel, legend = True):
    """
    General graph organization for titles and legends

    Parameters
    ----------
    title : string
        the title to name the graph.
    xlabel : string
        the label to give the x axis.
    ylabel : string
        the label to give the y axis.

    Returns
    -------
    None.

    """
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()


def plot_scatter(opening_dict, color = "black", label = None, graph = True):
    """
    Plots a scatterplot with a line of best fit for a set of data 
    found in the dictionary

    Parameters
    ----------
    opening_dict : dict
        dictionary containing the openings and corresponding data.
    color : string, optional
        the color to plot the points and line as. The default is "black".
    label : string, optional
        the label to use for the legend. The default is None.
    graph : boolean, optional
        determines user preferences on graph organization. 
        The default is True.

    Returns
    -------
    None.

    """
    legend_count = 0
    
    # create initial lists for line of best fit
    x_vals = []
    y_vals = []
    
    # loops through every opening in the dictionary
    for opening in opening_dict:
        
        # checks if the legend label has been added yet
        if legend_count == 0:
            
            # plots one point with the legend label
            plt.plot(opening_dict[opening][0], opening_dict[opening][1], 
                 marker = "o", color = color, label = label, alpha = 0.5)
            legend_count += 1
            
            # appends x and y values for line of best fit 
            x_vals.append(opening_dict[opening][0])
            y_vals.append(opening_dict[opening][1])
            
        else:
            
            # plots the point without the label once label is added
            plt.plot(opening_dict[opening][0], opening_dict[opening][1], 
                 marker = "o", color = color, alpha = 0.5)
            
            # appends x and y values for line of best fit      
            x_vals.append(opening_dict[opening][0])
            y_vals.append(opening_dict[opening][1])
            
            
    # create data for line of best fit using numpy built in functions
    x = np.array(x_vals)
    y = np.array(y_vals)
    m, b = np.polyfit(x, y, 1)
    
    # creates line of best fit as a string to allow it to be added to legend
    lobf_as_str = str(round(m, 2)) + " * x + " + str(round(b, 2))

    # plot line of best fit
    plt.plot(x, m * x + b, color = color, label = lobf_as_str)
    
    # checks plan of user for whether to show graph yet
    if graph:
        
        graph_organization("Chess Openings Success", 
                           "White Wins with Opening", 
                           "Black Wins with Opening")


def get_perc(dic, val_idx, total_val_idx):
    """
    Gets a percentage of two values in a dictionary

    Parameters
    ----------
    dic : dictionary
        dictionary containg the data to get a percentage.
    val_idx : int
        the index of the value to take as the percent.
    total_val_idx : int
        the index of the total games to take the percentage of.

    Returns
    -------
    perc : float
        the percentage return of the two values.

    """
    val_count = 0
    total_count = 0
    
    # loops through every index in the dictionary
    for i in dic:
        
        # adds the value count of the index to the total count of the value
        val_count += dic[i][val_idx]
        
        # adds the total count of the index to the total count of the total
        total_count += dic[i][total_val_idx]
    
    # gets the percentage of the value
    perc = round((val_count / total_count) * 100, 2)
    
    return perc


def Chess():
    
    print("Welcome to my chess project!\n")
    df = read_csv(CHESS)
    
    # clean the data to prepare for analyzing
    df = df_cleaning(df)
    
    # split into 3 groups of rating (> 1400, 1400-1800, < 1800)
    beginners = by_rating(df, 0, 1400, True)
    intermediate = by_rating(df, 1400, 1800, True)
    advanced = by_rating(df, 1800, 4000)
    
    # organize by opening {opening: [white wins, black wins, draws, games]}
    beg_openings = split_openings(beginners)
    int_openings = split_openings(intermediate)
    adv_openings = split_openings(advanced)
    
    # graph winning percentages by opening for white and black separately
    plot_scatter(beg_openings, "seagreen", "Beginner (0-1399)")
    plot_scatter(int_openings, "goldenrod", "Intermediate (1400-1799)")
    plot_scatter(adv_openings, "lightcoral", "Advanced (1800+)")
    
    # graph winning percentages by opening for white and black on same plot
    plot_scatter(beg_openings, "seagreen", "Beginner (0-1399)", False)
    plot_scatter(int_openings, "goldenrod", "Intermediate (1400-1799)", False)
    plot_scatter(adv_openings, "lightcoral", "Advanced (1800+)", False)
    graph_organization("Chess Openings Success at Varying Levels", 
                       "White Wins with Opening", 
                       "Black Wins with Opening")
    
    # compare white vs black win percentages at different levels
    white_beg_perc = get_perc(beg_openings, 0, 3)
    black_beg_perc = get_perc(beg_openings, 1, 3)
    print("Beginners white win %:", white_beg_perc, "%")
    print("Beginners black win %:", black_beg_perc, "%\n")
    
    white_int_perc = get_perc(int_openings, 0, 3)
    black_int_perc = get_perc(int_openings, 1, 3)
    print("Intermediate white win %:", white_int_perc, "%")
    print("Intermediate black win %:", black_int_perc, "%\n")
    
    white_adv_perc = get_perc(adv_openings, 0, 3)
    black_adv_perc = get_perc(adv_openings, 1, 3)
    print("Advanced white win %:", white_adv_perc, "%")
    print("Advanced black win %:", black_adv_perc, "%\n")
    
    # compare draw percentages at different levels
    beg_draw_perc = get_perc(beg_openings, 2, 3)
    print("Beginners draw %:", beg_draw_perc, "%\n")
    
    int_draw_perc = get_perc(int_openings, 2, 3)
    print("Intermediate draw %:", int_draw_perc, "%\n")
    
    adv_draw_perc = get_perc(adv_openings, 2, 3)
    print("Advanced draw %:", adv_draw_perc, "%\n")
    
    
if __name__ == "__main__":
    
    Chess()
