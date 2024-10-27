//
//  net_messages.h
//  GameServerOne
//
//  Created by Jérôme Delvenne on 7/10/24.
//

#define NOK_CLIENT_VERSION "ERR_CLIENT_VERSION"
#define OK_CLIENT_VERSION  "ACK_HANDSHAKE"
#define PING_ACK           "ACK_PING"
#define CLIENT_POS_ACK     "ACK_POSITION"
#define CLIENT_POS_NOK     "ERR_POSITION"

#define GAME_START_ACK     "ACK_GAME_START"
#define GAME_END_ACK       "ACK_GAME_END"
#define DMG_ACK            "ACK_DAMAGE"

#define Q1_ACK             "ACK_Q1"
#define Q2_ACK             "ACK_Q2"


#define GAME_FLAG          "Hero{ready_to_hack_world_of_warcraft}"
#define GAME_NO_FLAG       "You haven't done all the quests :("
