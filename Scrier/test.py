def countGroups(related):
    # Write your code here
    groups = {}
    for person in range(len(related)):
        relations = related[person]

        person_in_group = False
        for group_leader in groups:
            if person in groups[group_leader]:
                person_in_group = True
                break

        if not person_in_group:  # Then they'll be a group leader
            groups[person] = []
            group_leader = person

        for other_person in range(len(relations)):
            if (other_person != person) and (int(relations[other_person]) == 1) and (
                    other_person not in groups[group_leader]):
                groups[group_leader].append(other_person)

    return len(groups)

print(countGroups(['11000', '01100', '00100', '00010', '00011']))