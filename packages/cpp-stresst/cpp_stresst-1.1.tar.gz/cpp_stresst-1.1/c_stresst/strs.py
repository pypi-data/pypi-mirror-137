import argparse
import os
import subprocess


def main():
    prser = argparse.ArgumentParser(description="stress test a program with multiple inputs")
    prser.add_argument("file", metavar="prgm.cpp", type=str, nargs=1, help="program to test")
    prser.add_argument("test", metavar="testdir", type=str, nargs=1, help="directory of test cases")
    prser.add_argument("--w", help="compile on windows os", action="store_true")

    args = prser.parse_args()

    wa = True

    if (os.path.exists(os.path.join(os.path.abspath(os.getcwd()), str(args.file[0])))
            and os.path.exists(os.path.join(os.path.abspath(os.getcwd()), str(args.test[0])))):
        wa = False
        subprocess.Popen(["g++", str(args.file[0])])
        for sb, _, f in os.walk(os.path.join(os.path.abspath(os.getcwd()), str(args.test[0]))):
            for i in f:
                pth = sb + os.sep + i
                if pth.endswith(".in"):
                    with open(pth, "r", encoding="utf-8") as fin:

                        if (args.w):
                            p = subprocess.Popen([".\\a"], stdin=fin, stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                        else:
                            p = subprocess.Popen(["./a.out"], stdin=fin, stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                        out, err = p.communicate()
                        if not err:
                            out = str(out.decode("utf-8").strip())
                            arr = [o for o in os.listdir(str(args.test[0]))]

                            fn = i[:i.index(".")] + ".out"

                            if fn not in arr:
                                print("no output file for", i)
                                break

                            of = open(sb + os.sep + fn, "r", encoding="utf-8")
                            correct = str(of.read().strip())
                            out = out.replace('\n', '')
                            correct = correct.replace('\n', '')
                            if str(out) != str(correct):
                                print("Wrong Answer on", i)
                                print("Output:\n" + str(out), file=open("tf.txt", "w"))
                                print("Expected:\n" + str(correct), file=open("tf.txt", "a"))
                                wa = True
                                break
                        else:
                            print("Runtime Error on", i)
                            print(err)
                            wa = True
                            break
    else:
        print("Files not found")
    if not wa:
        print("All cases passed.")
