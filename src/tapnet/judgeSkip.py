import math
import argparse

from pymarl2.src.tapnet.models import TapNet
import torch
import numpy as np
from pymarl2.src.tapnet import Hyperparameter

def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

def load_tapnet_mode():
    parser = argparse.ArgumentParser()
    # cuda settings
    parser.add_argument('--seed', type=int, default=42, help='Random seed.')
    # Model parameters
    parser.add_argument('--use_cnn', type=boolean_string, default=True,
                        help='whether to use CNN for feature extraction. Default:False')
    parser.add_argument('--use_lstm', type=boolean_string, default=True,
                        help='whether to use LSTM for feature extraction. Default:False')
    parser.add_argument('--use_rp', type=boolean_string, default=True,
                        help='Whether to use random projection')
    parser.add_argument('--rp_params', type=str, default='-1,3',
                        help='Parameters for random projection: number of random projection, '
                             'sub-dimension for each random projection')
    parser.add_argument('--use_metric', action='store_true', default=False,
                        help='whether to use the metric learning for class representation. Default:False')
    parser.add_argument('--filters', type=str, default="256,256,128",
                        help='filters used for convolutional network. Default:256,256,128')
    parser.add_argument('--kernels', type=str, default="4,3,1",
                        help='kernels used for convolutional network. Default:4,3,1')
    parser.add_argument('--dilation', type=int, default=1,
                        help='the dilation used for the first convolutional layer. '
                             'If set to -1, use the automatic number. Default:-1')
    parser.add_argument('--layers', type=str, default="500,300",
                        help='layer settings of mapping function. [Default]: 500,300')
    parser.add_argument('--dropout', type=float, default=0,
                        help='Dropout rate (1 - keep probability). Default:0.5')
    parser.add_argument('--lstm_dim', type=int, default=256,
                        help='Dimension of LSTM Embedding.')
    args = parser.parse_args()

    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)
    args.sparse = True
    args.layers = [int(l) for l in args.layers.split(",")]
    args.kernels = [int(l) for l in args.kernels.split(",")]
    args.filters = [int(l) for l in args.filters.split(",")]
    args.rp_params = [float(l) for l in args.rp_params.split(",")]

    # update random permutation parameter
    if args.rp_params[0] < 0:
        dim = Hyperparameter.Steps
        args.rp_params = [3, math.floor(dim / (3 / 2))]
    else:
        dim = Hyperparameter.Steps
        args.rp_params[1] = math.floor(dim / args.rp_params[1])

    args.rp_params = [int(l) for l in args.rp_params]

    # update dilation parameter
    our_side_num, enemy_num = [], []
    if Hyperparameter.game_scene == '3s_vs_3z':
        our_side_num, enemy_num = Hyperparameter.our_side_num_3s_vs_3z, Hyperparameter.enemy_num_3s_vs_3z
    elif Hyperparameter.game_scene == '2m_vs_1z':
        our_side_num, enemy_num = Hyperparameter.our_side_num_2m_vs_1z, Hyperparameter.enemy_num_2m_vs_1z
    DIMENSION = (our_side_num + enemy_num) * 2

    if args.dilation == -1:
        args.dilation = math.floor(DIMENSION / 64)

    model = TapNet(nfeat=Hyperparameter.Steps,
                   len_ts=DIMENSION,
                   layers=args.layers,
                   nclass=Hyperparameter.nclass,
                   dropout=args.dropout,
                   use_lstm=args.use_lstm,
                   use_cnn=args.use_cnn,
                   filters=args.filters,
                   dilation=args.dilation,
                   kernels=args.kernels,
                   use_metric=args.use_metric,
                   use_rp=args.use_rp,
                   rp_params=args.rp_params,
                   lstm_dim=args.lstm_dim
                   )
    return model

def predict_one(model, seq):
    model.eval()

    bench_noCrash = Hyperparameter.bench_noCrash

    siameseP1 = [bench_noCrash]
    siameseP2 = [seq]

    if Hyperparameter.GPU_USED:
        siameseP1 = torch.FloatTensor(np.array(siameseP1)).cuda()
        siameseP2 = torch.FloatTensor(np.array(siameseP2)).cuda()
    else:
        siameseP1 = torch.FloatTensor(np.array(siameseP1)).cpu()
        siameseP2 = torch.FloatTensor(np.array(siameseP2)).cpu()
    output1 = model(siameseP1, siameseP2)
    output1 = torch.nn.Sigmoid()(output1)

    THRESHOLD = 0
    if Hyperparameter.game_scene == '3s_vs_3z':
        THRESHOLD = Hyperparameter.threshold_3s_vs_3z
    elif Hyperparameter.game_scene == '2m_vs_1z':
        THRESHOLD = Hyperparameter.threshold_2m_vs_1z

    if output1[0][0] > THRESHOLD:
        return 1
    else:
        return 0