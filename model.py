import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import datetime

def classify(game_title_input):
    # game_store = 'Steam'

    df_hist_merge_1 = pd.read_csv('df_hist_merge.csv')

    df_hist_merge_1 = df_hist_merge_1.set_index('Unnamed: 0')
    df_hist_merge_1['game_date'] = pd.to_datetime(df_hist_merge_1.game_date)

    df_game = df_hist_merge_1.loc[(df_hist_merge_1.stores_title == game_title_input)]
    sales_game = df_game.groupby('game_date')['stores_title'].count().reset_index()

    dates = pd.date_range(sales_game.game_date.min(), df_hist_merge_1.game_date.max(), name='game_date').date

    sales_game = sales_game.set_index('game_date').reindex(dates)
    sales_game = sales_game.asfreq('D')

    # Replace any non-sales day with a 0
    sales_game['stores_title'] = np.where(sales_game.stores_title.isnull() == True,
                                          0,
                                          1)

    # Create values
    sales_game = sales_game.reset_index()
    x = sales_game.index.values
    y = sales_game.stores_title.values

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


    # Apply predictions over next 30 days
    # Create next 30 days
    predict_30 = pd.date_range(df_hist_merge_1.game_date.max() + datetime.timedelta(days=1),
                               df_hist_merge_1.game_date.max() + datetime.timedelta(days=30))
    df_predict_30 = pd.DataFrame({'game_date': predict_30})

    # Apply model
    sale_game_next = sales_game.append(df_predict_30).reset_index().drop('index', axis=1)
    pred_30 = sale_game_next.iloc[-len(predict_30):].index.values.reshape(-1, 1)
    next_pred = model.predict(pred_30)

    # Insert predictions to df
    df_predict_30['pred'] = next_pred

    # Make statement
    if df_predict_30.loc[df_predict_30.pred == 1]['game_date'].shape[0] > 0:
        result = "There may be a sale for " + game_title_input + " over the next 30 days. This model has a " + str(round(metrics.accuracy_score(y_test, y_pred), 2)*100) + "% accuracy."
    else:
        result = "There may NOT be a sale for " + game_title_input + " over the next 30 days. This model has a " + str(round(metrics.accuracy_score(y_test, y_pred), 2)*100) + "% accuracy."

    return result
