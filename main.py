import yaml
import json
import sys


def get_dict_list(target, k, v):
    for t in target:
         if t[k] == v:
             return t

def print_json(target):
    print(json.dumps(target, indent=4, sort_keys=True))

def print_dict(target):
    print(json.dumps(target, indent=4, sort_keys=True))

def getnerate_iam_policy():
    with open("roles.yaml", "r") as rf:
        roles = yaml.load(rf)
        
    with open("users.yaml", "r") as uf:
        users = yaml.load(uf)

    iam_policies = []
    for role in roles:
        pj_role, iam_roles = role.popitem()
        pj_role_users = users[pj_role]
        for iam_role in iam_roles:
            for user in pj_role_users:
                iam_policy = get_dict_list(iam_policies, 'role', iam_role)
                if iam_policy is None:
                    iam_policies.append({'role': iam_role, 'members': [user]})
                else:
                    iam_policy['members'].append(user)
    return iam_policies

def merge_iam(iam_policies):
    with open("iam.json", "r") as f:
        origin = json.load(f)

    #print_json(origin)

    bindings = origin["bindings"]

    for iam_policy in iam_policies:
        bind = get_dict_list(bindings, 'role', iam_policy['role'])
        if bind == None:
            bindings.append({'role': iam_policy['role'], 'members':iam_policy['members']})
        else:
            bind['members'].extend(iam_policy['members'])

    print_json(origin)

def main():
    policies = getnerate_iam_policy()
    merge_iam(policies)

if __name__ == '__main__':
    sys.exit(main())
