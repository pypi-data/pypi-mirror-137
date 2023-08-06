import os
import cv2
import shutil
import subprocess
from argparse import ArgumentParser


neg_list = "neg.lst"
pos_list = "pos.lst"
vec_file = "samples.vec"
createsamples_path = f"{os.path.dirname(__file__)}/data/opencv_createsamples.exe"
traincascade_path = f"{os.path.dirname(__file__)}/data/opencv_traincascade.exe"

parser = ArgumentParser()
parser.add_argument("-neg", "--negative", help="Negatives path", required=True)
parser.add_argument("-pos", "--positive", help="Positives path", required=True)
parser.add_argument(
    "-w", "--width", help="Sample width", type=int, required=False, default=25
)
parser.add_argument(
    "-he", "--height", help="Sample height", type=int, required=False, default=25
)
parser.add_argument(
    "-s", "--stages", help="Number of stages", type=int, required=False, default=20
)
parser.add_argument(
    "-t", "--numThreads", help="Number of threads", type=int, required=False, default=2
)
parser.add_argument(
    "-b",
    "--accaptanceRatioBreakValue",
    help="Accaptance ratio break value",
    type=float,
    default=-1,
)
parser.add_argument(
    "--idxSize",
    help="Size of buffer for precalculated feature indices (in Mb)",
    type=int,
    required=False,
    default=1024,
)
parser.add_argument(
    "--valSize",
    help="Size of buffer for precalculated feature values (in Mb)",
    type=int,
    required=False,
    default=1024,
)
parser.add_argument(
    "-m",
    "--mode",
    help="Feature mode",
    required=True,
    choices=["BASIC", "CORE", "ALL"],
    default="BASIC",
)
parser.add_argument(
    "-npt",
    "--numPosTrain",
    help="Number of positives for training. This should be less than numPosVec",
    type=int,
    required=True,
)
parser.add_argument(
    "-npv",
    "--numPosVec",
    help="Number of positives for creating vector file",
    type=int,
    required=True,
)
parser.add_argument(
    "-nn", "--numNeg", help="Number of negatives", type=int, required=True
)
parser.add_argument(
    "-o", "--output", help="Output folder", required=False, default="classifier"
)

args = parser.parse_args()

neg_path = os.path.relpath(args.negative).replace("\\", "/")
neg_files = os.listdir(neg_path)
pos_path = os.path.relpath(args.positive).replace("\\", "/")
pos_files = os.listdir(pos_path)


def main():
    remove_files()
    create_lists()
    create_vec()
    train_cascade()


def remove_files():
    if os.path.isfile(neg_list):
        os.remove(neg_list)
    if os.path.isfile(pos_list):
        os.remove(pos_list)
    if os.path.isfile(vec_file):
        os.remove(vec_file)


def create_lists():
    for file in neg_files:
        raw_neg = neg_path + "/" + file
        neg = raw_neg.replace(" ", "_")
        os.rename(raw_neg, neg)
        if neg.endswith((".jpg", ".jpeg", ".png")):
            with open(neg_list, "a") as f:
                f.write(neg + "\n")

    for file in pos_files:
        raw_pos = pos_path + "/" + file
        pos = raw_pos.replace(" ", "_")
        os.rename(raw_pos, pos)
        if pos.endswith((".jpg", ".jpeg", ".png")):
            w, h = cv2.imread(pos).shape[:2]
            arg0 = f"{pos} 1 0 0 {w} {h}"
            with open(pos_list, "a") as f:
                f.write(arg0 + "\n")


def create_vec():
    command = f"{createsamples_path} -info {pos_list} -vec {vec_file} -w {args.width} -h {args.height} -num {args.numPosVec}"
    print(command)
    subprocess.call(command.split(" "), shell=False)


def train_cascade():
    if os.path.isdir(args.output):
        shutil.rmtree(args.output)
    os.mkdir(args.output)

    if args.accaptanceRatioBreakValue == -1.0:
        arbv = -1
    else:
        arbv = args.accaptanceRatioBreakValue

    command = f"{traincascade_path} -data {args.output} -vec {vec_file} -bg {neg_list} -numPos {args.numPosTrain} -numNeg {args.numNeg} -numStages {args.stages} -w {args.width} -h {args.height} -precalcIdxBufSize {args.idxSize} -precalcValBufSize {args.valSize} -numThreads {args.numThreads} -acceptanceRatioBreakValue {arbv} -mode {args.mode}"
    print(command)
    subprocess.call(command.split(" "), shell=False)
