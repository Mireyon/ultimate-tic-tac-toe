# from keras.layers import Input, Dense, Flatten, Reshape, Conv2D
# from keras.models import Model
# from keras.optimizers import Adam
import pandas as pd
import os

# def create_model():
#     input_layer = Input(shape=(9,9), name="board")
#     x = Reshape((9,9,1))(input_layer)
#     conv2D_layer = Conv2D(128, (3,3), padding='valid', activation='relu', name='conv_1')(x)
#     conv2D_layer = Conv2D(128, (3,3), padding='valid', activation='relu', name='conv_2')(conv2D_layer)
#     conv2D_layer = Conv2D(128, (3,3), padding='valid', activation='relu', name='conv_3')(conv2D_layer)

#     flatten_layer = Flatten()(conv2D_layer)
#     dense_layer = Dense(512, activation='relu', name='dense_1')(flatten_layer)
#     dense_layer = Dense(256, activation='relu', name='dense_2')(dense_layer)

#     pi = Dense(81, activation='relu', name='pi')(dense_layer)
#     value = Dense(1, activation='relu', name='value')(dense_layer)

#     model = Model(inputs=input_layer, outputs=[pi, value])
#     model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(0.001))

#     model.summary()
#     return model

class Data:
    if os.path.exists("../results/data.csv"):
        data = pd.read_csv("../results/data.csv", sep=";")
    else:
        data = pd.DataFrame(columns = ['state', 'policy', 'value'])
    states = []
    pis = []
    value = None

    @staticmethod
    def add(state, pi):
        Data.states.append(state)
        Data.pis.append(pi)

    @staticmethod
    def clear():
        Data.data = pd.read_csv("../results/data.csv", sep=";")
        Data.states = []
        Data.pis = []
        Data.value = None

    @staticmethod
    def write_csv(state, pi):
        Data.data = pd.concat([Data.data, pd.DataFrame([[state, pi, Data.value]], columns=Data.data.columns)], ignore_index=True)