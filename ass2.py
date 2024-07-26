from collections import deque, defaultdict

class SocialNetwork:
    def __init__(self):
        self.network = defaultdict(set)

    def add_friendship(self, person1, person2):
        self.network[person1].add(person2)
        self.network[person2].add(person1)

    def find_friends(self, person):
        return self.network[person]

    def find_common_friends(self, person1, person2):
        return self.network[person1] & self.network[person2]

    def find_nth_connection(self, person1, person2):
        if person1 == person2:
            return 0
        
        visited = set()
        queue = deque([(person1, 0)])
        
        while queue:
            current_person, depth = queue.popleft()
            visited.add(current_person)
            
            for friend in self.network[current_person]:
                if friend == person2:
                    return depth + 1
                if friend not in visited:
                    queue.append((friend, depth + 1))
                    visited.add(friend)
        
        return -1

if __name__ == "__main__":
    social_network = SocialNetwork()
    
    # Adding friendships
    social_network.add_friendship("Alice", "Bob")
    social_network.add_friendship("Bob", "Janice")
    social_network.add_friendship("Alice", "Eve")
    social_network.add_friendship("Bob", "Charlie")
    social_network.add_friendship("Charlie", "David")
    
    # Find all friends of Alice and Bob
    alice_friends = social_network.find_friends("Alice")
    bob_friends = social_network.find_friends("Bob")
    
    print(f"Friends of Alice: {alice_friends}")
    print(f"Friends of Bob: {bob_friends}")
    
    # Find common friends of Alice and Bob
    common_friends = social_network.find_common_friends("Alice", "Bob")
    print(f"Common friends of Alice and Bob: {common_friends}")
    
    # Find nth connection
    connection1 = social_network.find_nth_connection("Alice", "Janice")
    connection2 = social_network.find_nth_connection("Alice", "Charlie")
    connection3 = social_network.find_nth_connection("Alice", "David")
    connection4 = social_network.find_nth_connection("Alice", "Alice")
    connection5 = social_network.find_nth_connection("Alice", "Frank")
    
    print(f"Connection between Alice and Janice: {connection1}")
    print(f"Connection between Alice and Charlie: {connection2}")
    print(f"Connection between Alice and David: {connection3}")
    print(f"Connection between Alice and Alice: {connection4}")
    print(f"Connection between Alice and Frank: {connection5}")
