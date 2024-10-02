import config

if __name__ == "__main__":
    if not config.COMPONENT:
        print("COMPONENT is not set")
        exit(1)
    
    match config.COMPONENT:
        case 'discord-bot':
            from app.discord import main as bot
            bot.main()
        case _:
            print("Unknown component")
            exit(1)
