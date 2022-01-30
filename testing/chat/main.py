from chatroom import Chatroom, Guest
# global
flight = "ABCD1234"

room = Chatroom(flight)

guest1 = Guest("Chris")

room.addGuest(guest1)

print("////////////////////\nTHIS IS YOUR FLIGHT")
print(room.flight())


print(room.guestNum())
guests = room.guestList()
for guest in guests:
    print(guest.name)
