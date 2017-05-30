from math import sqrt


# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # if they have no ratings in common, return 0
    if len(si) == 0:
        return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sum_of_squares)


# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0:
        return 0

    # Sum calculations
    n = len(si)

    # sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sums of the squares
    sum1sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum of the products
    psum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num = psum - (sum1 * sum2 / n)
    den = sqrt((sum1sq - pow(sum1, 2) / n) * (sum2sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    r = num / den

    return r


# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def get_recommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simsums = {}
    for other in prefs:

        # don't compare me to myself
        if other == person:
            continue

        sim = similarity(prefs, person, other)

        # ignore scores of zero or lower
        if sim <= 0:
            continue

        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simsums.setdefault(item, 0)
                simsums[item] += sim

    # Create the normalized list
    rankings = [(total / simsums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


def transform_prefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            # Flip item and person
            result[item][person] = prefs[person][item]
    return result


def calculate_similar_items(prefs, n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result = {}
    # Invert the preference matrix to be item-centric
    item_prefs = transform_prefs(prefs)
    c = 0
    for item in item_prefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0:
            print("%d / %d" % (c, len(item_prefs)))
        # Find the most similar items to this one
        scores = top_matches(item_prefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


def get_recommended_items(prefs, item_match, user):
    user_ratings = prefs[user]
    scores = {}
    total_sim = {}
    # Loop over items rated by this user
    for (item, rating) in user_ratings.items():

        # Loop over items similar to this one
        for (similarity, item2) in item_match[item]:

            # Ignore if this user has already rated this item
            if item2 in user_ratings:
                continue

            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            # Sum of all the similarities
            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity

    # Divide each total score by total weighting to get an average
    rankings = [(score / total_sim[item], item) for item, score in scores.items()]

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings
