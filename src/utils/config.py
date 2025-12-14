distractor_apps = [
    # Videojuegos y plataformas de juegos
    "Steam.exe",            # Cliente de Steam (plataforma de juegos)
    "SteamService.exe",     # Servicio de Steam
    "EpicGamesLauncher.exe",# Epic Games Launcher
    "GalaxyClient.exe",     # GOG Galaxy Client
    "Battle.net.exe",       # Blizzard Battle.net
    "Uplay.exe",           # Ubisoft Uplay
    "Origin.exe",          # EA Origin
    "Launcher.exe",        # Genérico para varios juegos
    "FortniteClient-Win64-Shipping.exe",  # Fortnite
    "FortniteClient-Win64-Shipping_EAC.exe", # Fortnite con anti-trampas
    "MinecraftLauncher.exe",# Lanzador de Minecraft:contentReference[oaicite:5]{index=5}
    "javaw.exe",           # Máquina virtual de Java (usado por Minecraft Java Edition)
    "RobloxPlayerBeta.exe",# Cliente de Roblox (juego):contentReference[oaicite:6]{index=6}
    "RobloxStudioBeta.exe",# Editor de Roblox (juego):contentReference[oaicite:7]{index=7}
    "epicgameslauncher.exe",# (alias de EpicGamesLauncher.exe)
    "Steam.exe",           # (repetido para énfasis)
    "Launcher.exe",        # (varios juegos comparten ejecutable genérico)
    "AceOfSpades.exe",     # Ejemplo de juego (Ace of Spades)
    "Among Us.exe",        # Among Us
    "Skyrim.exe",          # The Elder Scrolls V: Skyrim
    "TESV.exe",            # Skyrim, variante
    "witcher3.exe",        # The Witcher 3
    "witcher.exe",         # The Witcher Enhanced Edition
    "rocketleague.exe",    # Rocket League
    "rocketleague.exe",    # (variante 32-bit)
    "gtav.exe",            # Grand Theft Auto V (alias)
    "gtavlauncher.exe",    # GTA V launcher
    "gta_sa.exe",          # GTA: San Andreas
    "gta3.exe",            # GTA III
    "gta-vc.exe",          # GTA: Vice City
    "leagueclientux.exe",  # League of Legends (cliente)
    "valorant.exe",        # Valorant (Riot Games)
    "r5apex.exe",         # Apex Legends
    "RiotClientServices.exe",  # Servicio de Riot Games
    "vgc.exe",            # Servicio anti-trampas (Valorant)
    "launcer.exe",         # Posible genérico
    "dota2.exe",           # Dota 2
    "hl2.exe",             # Half-Life 2 / Counter-Strike (uso compartido)
    "hl.exe",              # Half-Life / Counter-Strike
    "csgo.exe",           # Counter-Strike: Global Offensive
    "cs2.exe",            # Counter-Strike 2 (CS2, aún en desarrollo)
    "hl2.exe",            # CS:Source (usa hl2.exe)
    "iw4mp.exe",          # CoD MW2
    "iw4sp.exe",          # CoD MW2 singleplayer
    "iw5mp.exe",          # CoD MW3 MP
    "iw5sp.exe",          # CoD MW3 SP
    "blackops.exe",       # CoD Black Ops MP (t6mp.exe)
    "t6zm.exe",          # CoD Black Ops II Zombies
    "iw7_ship.exe",       # CoD Infinite Warfare
    "s2_sp64_ship.exe",   # CoD WWII
    "payday2_win32_release.exe", # Payday 2
    "payday_win32_release.exe",  # Payday: The Heist
    "paladins.exe",      # Paladins
    "paladins.exe",      # (alias)
    "battalionlauncher.exe", # Battalion 1944
    "minecraft.exe",     # Cliente de Minecraft (Bedrock Edition en Windows)
    "osu!.exe",          # osu! (juego de ritmo)
    "gta5.exe",          # alias para GTA V
    "gta5.exe",          # alias repetido
    "Persona.exe",       # Persona 5
    "genshinimpact.exe", # Genshin Impact
    # Plataformas de streaming y multimedia (como apps de ocio)
    "Spotify.exe",       # Reproductor de música Spotify
    "Twitch.exe",        # Aplicación de Twitch
    "Netflix.exe",       # (si existiera como app UWP; se incluye por si aplica)
    "YouTubeMusic.exe",  # (posible cliente UWP)
    # Redes sociales y mensajería
    "Discord.exe",       # Discord (chat de voz/voip para gamers):contentReference[oaicite:8]{index=8}
    "DiscordPTB.exe",    # Discord Public Test Build
    "DiscordCanary.exe", # Discord Canary
    "Slack.exe",         # Slack
    "WhatsApp.exe",      # WhatsApp Desktop
    "Telegram.exe",      # Telegram Desktop
    "Messenger.exe",     # Facebook Messenger
    "Facebook.exe",      # App de Facebook
    "Instagram.exe",     # App de Instagram (Windows)
    "TikTok.exe",        # App de TikTok (si existe)
    "WeChat.exe",        # WeChat Desktop
    "Signal.exe",        # Signal Desktop
    "Snapchat.exe",      # (si existiera versión desktop)
    "Line.exe",          # LINE
    "Skype.exe",         # Skype
    "Teams.exe",         # Microsoft Teams
    "Zoom.exe",          # Zoom
    # Edición multimedia / aplicaciones creativas
    "Photoshop.exe",     # Adobe Photoshop
    "Illustrator.exe",   # Adobe Illustrator
    "Premiere.exe",      # Adobe Premiere Pro
    "AfterFX.exe",       # Adobe After Effects
    "GIMP.exe",         # GIMP (editor de imágenes)
    "PaintDotNet.exe",   # Paint.NET
    "Audacity.exe",      # Audacity (edición de audio)
    "FLStudio.exe",      # FL Studio (producción musical)
    "AbletonLive.exe",   # Ableton Live (producción musical)
    "obs32.exe",         # OBS Studio 32-bit
    "obs64.exe",         # OBS Studio 64-bit
    "CamtasiaStudio.exe",# Camtasia (grabación/video)
    "DaVinciResolve.exe",# DaVinci Resolve (video edición)
    "Vegas.exe",         # Sony Vegas
    "AfterEffects.exe",  # alias de AfterFX
    "Final Cut Pro.exe", # (en mac no aplica, ignorar en Windows)
    # Otros ejemplos comunes de ocio/descarga
    "uTorrent.exe",      # uTorrent (cliente torrent)
    "BitTorrent.exe",    # BitTorrent client
    "qBittorrent.exe",   # qBittorrent client
    "VLC.exe",          # VLC media player (muy popular para video)
]

# Alias para compatibilidad
BLOCKED_APPS = distractor_apps

# Tiempo de advertencia antes de cerrar (en segundos)
WARNING_TIME = 3

# Intervalo de revisión (en segundos)
CHECK_INTERVAL = 5
