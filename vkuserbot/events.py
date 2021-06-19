from .tools import VkuserbotClass

class Events(VkuserbotClass):
    NewMessage = 4
    EditMessage = 5
    FriendOnline = 8
    FriendOffline = 9
    RemoveMessage = 13
    RecoveryMessage = 14
    ChangeChatSettings = 51
    UserWriting = 61
    UserWritingChat = 62
    UsersWriting = 63
    RecordAudioMessage = 64
    CallEvent = 70
