import glob

class CountMutators():

    def parse_file(self, path):
        totalMutants = 0
        totalMutantsKilled = 0
        mutantReturnValsMutator = 0
        mutantReturnValsMutatorKilled = 0
        mutantNegateConditionalsMutator = 0
        mutantNegateConditionalsMutatorKilled = 0
        mutantVoidMethodCallMutator = 0
        mutantVoidMethodCallMutatorKilled = 0
        mutantConditionalsBoundaryMutator = 0
        mutantConditionalsBoundaryMutatorKiller = 0
        mutantIncrementsMutator = 0
        mutantIncrementsMutatorKilled = 0
        mutantMathMutator = 0
        mutantMathMutatorKilled = 0

        files = glob.glob(path)

        for i,file in enumerate(files):
            with open(files[i]) as fd:
                print(files[i])
                for line in fd:
                    if 'ReturnValsMutator' in line:
                        mutantReturnValsMutator += 1
                        if 'KILLED' in line:
                            mutantReturnValsMutatorKilled += 1
                    if 'NegateConditionalsMutator' in line:
                        mutantNegateConditionalsMutator += 1
                        if 'KILLED' in line:
                            mutantNegateConditionalsMutatorKilled += 1
                    if 'VoidMethodCallMutator' in line:
                        mutantVoidMethodCallMutator += 1
                        if 'KILLED' in line:
                            mutantVoidMethodCallMutatorKilled += 1
                    if 'ConditionalsBoundaryMutator' in line:
                        mutantConditionalsBoundaryMutator += 1
                        if 'KILLED' in line:
                            mutantConditionalsBoundaryMutatorKiller += 1
                    if 'IncrementsMutator' in line:
                        mutantIncrementsMutator += 1
                        if 'KILLED' in line:
                            mutantIncrementsMutatorKilled += 1
                    if 'MathMutator' in line:
                        mutantMathMutator += 1
                        if 'KILLED' in line:
                            mutantMathMutatorKilled += 1

                    totalMutants += 1
                    totalMutantsKilled += line.count('KILLED')
            print("total: %d" %totalMutants)
            print("total killed: %d" %totalMutantsKilled)

            fd.close()



        return totalMutants, \
               totalMutantsKilled, \
               mutantReturnValsMutator, \
               mutantReturnValsMutatorKilled, \
               mutantNegateConditionalsMutator, \
               mutantNegateConditionalsMutatorKilled, \
               mutantVoidMethodCallMutator, \
               mutantVoidMethodCallMutatorKilled, \
               mutantConditionalsBoundaryMutator, \
               mutantConditionalsBoundaryMutatorKiller, \
               mutantIncrementsMutator, \
               mutantIncrementsMutatorKilled, \
               mutantMathMutator, \
               mutantMathMutatorKilled

