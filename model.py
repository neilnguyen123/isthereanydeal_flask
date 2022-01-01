import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import datetime
from bs4_scrape import Scrape
import pipeline

def classify(game_title_input):
    today = pd.to_datetime(pd.datetime.today()).floor('D').strftime("%m/%d/%Y")

    df_final = pipeline.df_pipe(Scrape.scrape(game_title_input))
    # Create column to determine if sales or not
    df_final['sale'] = np.where(df_final.sale_duration.isnull() == True, 0, 1)

    # Create values
    df_final = df_final.reset_index()
    x = df_final.index.values
    y = df_final.sale.values

    # Test train split
    x_train, x_test, y_train, y_test = train_test_split(x,
                                                        y,
                                                        test_size=0.25,
                                                        random_state=0)

    # Train model
    model = LogisticRegression(solver='liblinear', random_state=0, C=0.05, multi_class='ovr')
    model.fit(x_train.reshape(-1, 1), y_train)

    # Create predictions from model
    y_pred = model.predict(x_test.reshape(-1, 1))

    # Make prediction over next 5 days
    predict_5 = pd.date_range(df_final.game_date.max() + datetime.timedelta(days=1),
                              df_final.game_date.max() + datetime.timedelta(days=5))
    df_predict_5 = pd.DataFrame({'game_date': predict_5})

    # Apply model
    sale_game_next = df_final.append(df_predict_5).reset_index().drop('index', axis=1)
    pred_5 = sale_game_next.iloc[-len(predict_5):].index.values.reshape(-1, 1)
    next_pred = model.predict(pred_5)

    # Insert predictions to df
    df_predict_5['pred'] = next_pred

    # Make statement
    if df_predict_5.loc[df_predict_5.pred == 1]['game_date'].shape[0] > 0:
        result = f"As of {today}, there may be a sale for {game_title_input} in the next 5 days on Steam. This model has a " + str(
            round(metrics.accuracy_score(y_test, y_pred), 2) * 100) + "% accuracy."
    else:
        result = f"As of {today}, there may be no sales for {game_title_input} in the next 5 days on Steam. This model has a " + str(
            round(metrics.accuracy_score(y_test, y_pred), 2) * 100) + "% accuracy."

    return result

# classify("The Elder Scrolls V: Skyrim")