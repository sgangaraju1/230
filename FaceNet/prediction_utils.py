
class Found:
    def __init__(self):
        self.found     = 0
        self.found_not = 0
        self.found_far = 0
        self.found_mis = 0

    def __str__(self):
        return "FOUND : " + str(self.found) + " " + str(self.found_not) + " " + str(self.found_far) + " " + str(self.found_mis)

    def total(self):
        return self.found + self.found_not + self.found_far + self.found_mis

    def tp(self):
        return self.found

    def tp_pct(self):
        return self.found / self.total() * 100

    def fn(self):
        return self.found_not + self.found_far

    def fn_pct(self):
        return self.fn() / self.total() * 100

    def fp(self):
        return self.found_mis

    def fp_pct(self):
        return self.fp() / self.total() * 100

class ResultPredict:
    def __init__(self):
        self.total         = 0
        self.overall       = Found()
        self.gender_male   = Found()
        self.gender_female = Found()
        self.race_white    = Found()
        self.race_asian    = Found()
        self.race_black    = Found()

    def __str__(self):
        return str(self.total) + "\n" + str(self.overall) + "\n" + str(self.gender_male) + "\n" + str(self.gender_female)  + "\n" + str(self.race_white) + "\n" + str(self.race_asian) + "\n" + str(self.race_black)

def predict(neighbors, distance_threshold, attributes, train_set_x, train_set_y, other_set_x, other_set_y):
    ret       = ResultPredict()
    ret.total = len(other_set_x)
    persons   = attributes.Person.unique()

    for i in range(len(other_set_x)):
        other_emd   = other_set_x[i]
        other_label = other_set_y[i]

        other_attributes = None
        if (other_label in persons):
            other_attributes = attributes[attributes.Person == other_label].iloc[0]
            gender           = other_attributes.Gender
            race             = other_attributes.Race
            age              = other_attributes.Age

        distances, indices = neighbors.kneighbors([other_emd])

        if ((indices is None) or (len(indices) <= 0)):
            ret.overall.found_not += 1
            if (other_attributes is not None):
                if (gender == "MALE"):
                    ret.gender_male.found_not += 1
                else:
                    ret.gender_female.found_not += 1

                if (race == "WHITE"):
                    ret.race_white.found_not += 1
                elif (race == "ASIAN"):
                    ret.race_asian.found_not += 1
                else:
                    ret.race_black.found_not += 1
            continue

        dist = distances[0][0]
        if (dist > distance_threshold):
            ret.overall.found_far += 1
            if (other_attributes is not None):
                if (gender == "MALE"):
                    ret.gender_male.found_far += 1
                else:
                    ret.gender_female.found_far += 1

                if (race == "WHITE"):
                    ret.race_white.found_far += 1
                elif (race == "ASIAN"):
                    ret.race_asian.found_far += 1
                else:
                    ret.race_black.found_far += 1
            continue
        
        train_emd   = train_set_x[indices[0][0]]
        train_label = train_set_y[indices[0][0]]

        if (other_label != train_label):
            ret.overall.found_mis += 1
            if (other_attributes is not None):
                if (gender == "MALE"):
                    ret.gender_male.found_mis += 1
                else:
                    ret.gender_female.found_mis += 1

                if (race == "WHITE"):
                    ret.race_white.found_mis += 1
                elif (race == "ASIAN"):
                    ret.race_asian.found_mis += 1
                else:
                    ret.race_black.found_mis += 1
            continue

        if (gender == "MALE"):
            ret.gender_male.found += 1
        else:
            ret.gender_female.found += 1

        if (race == "WHITE"):
            ret.race_white.found += 1
        elif (race == "ASIAN"):
            ret.race_asian.found += 1
        else:
            ret.race_black.found += 1
        ret.overall.found += 1

    return ret

def show_metrics(result_predict):
    print("    total: {0:6d} ({1:6.2f} %)".format(result_predict.overall.total(), 100.00))
    print("    TP:    {0:6d} ({1:6.2f} %)".format(result_predict.overall.tp(), result_predict.overall.tp_pct()))
    print("    FN:    {0:6d} ({1:6.2f} %)".format(result_predict.overall.fn(), result_predict.overall.fn_pct()))
    print("    FP:    {0:6d} ({1:6.2f} %)".format(result_predict.overall.fp(), result_predict.overall.fp_pct()))

    print("MALE:")
    print("    total: {0:6d} ({1:6.2f} %)".format(result_predict.gender_male.total(), 100.00))
    print("    TP:    {0:6d} ({1:6.2f} %)".format(result_predict.gender_male.tp(), result_predict.gender_male.tp_pct()))
    print("    FN:    {0:6d} ({1:6.2f} %)".format(result_predict.gender_male.fn(), result_predict.gender_male.fn_pct()))
    print("    FP:    {0:6d} ({1:6.2f} %)".format(result_predict.gender_male.fp(), result_predict.gender_male.fp_pct()))

    print("FEMALE:")
    print("    total: {0:6d} ({1:6.2f} %)".format(result_predict.gender_female.total(), 100.00))
    print("    TP:    {0:6d} ({1:6.2f} %)".format(result_predict.gender_female.tp(), result_predict.gender_female.tp_pct()))
    print("    FN:    {0:6d} ({1:6.2f} %)".format(result_predict.gender_female.fn(), result_predict.gender_female.fn_pct()))
    print("    FP:    {0:6d} ({1:6.2f} %)".format(result_predict.gender_female.fp(), result_predict.gender_female.fp_pct()))

    print("WHITE:")
    print("    total: {0:6d} ({1:6.2f} %)".format(result_predict.race_white.total(), 100.00))
    print("    TP:    {0:6d} ({1:6.2f} %)".format(result_predict.race_white.tp(), result_predict.race_white.tp_pct()))
    print("    FN:    {0:6d} ({1:6.2f} %)".format(result_predict.race_white.fn(), result_predict.race_white.fn_pct()))
    print("    FP:    {0:6d} ({1:6.2f} %)".format(result_predict.race_white.fp(), result_predict.race_white.fp_pct()))

    print("ASIAN:")
    print("    total: {0:6d} ({1:6.2f} %)".format(result_predict.race_asian.total(), 100.00))
    print("    TP:    {0:6d} ({1:6.2f} %)".format(result_predict.race_asian.tp(), result_predict.race_asian.tp_pct()))
    print("    FN:    {0:6d} ({1:6.2f} %)".format(result_predict.race_asian.fn(), result_predict.race_asian.fn_pct()))
    print("    FP:    {0:6d} ({1:6.2f} %)".format(result_predict.race_asian.fp(), result_predict.race_asian.fp_pct()))
    
    print("BLACK:")
    print("    total: {0:6d} ({1:6.2f} %)".format(result_predict.race_black.total(), 100.00))
    print("    TP:    {0:6d} ({1:6.2f} %)".format(result_predict.race_black.tp(), result_predict.race_black.tp_pct()))
    print("    FN:    {0:6d} ({1:6.2f} %)".format(result_predict.race_black.fn(), result_predict.race_black.fn_pct()))
    print("    FP:    {0:6d} ({1:6.2f} %)".format(result_predict.race_black.fp(), result_predict.race_black.fp_pct()))
