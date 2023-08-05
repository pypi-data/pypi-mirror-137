import subprocess
import time

import coolname

ALL_ENVS = [
    "ALE/Adventure-v5",
    "ALE/AirRaid-v5",
    "ALE/Alien-v5",
    "ALE/Amidar-v5",
    "ALE/Assault-v5",
    "ALE/Asterix-v5",
    "ALE/Asteroids-v5",
    "ALE/Atlantis-v5",
    "ALE/Atlantis2-v5",
    "ALE/Backgammon-v5",
    "ALE/BankHeist-v5",
    "ALE/BasicMath-v5",
    "ALE/BattleZone-v5",
    "ALE/BeamRider-v5",
    "ALE/Berzerk-v5",
    "ALE/Blackjack-v5",
    "ALE/Bowling-v5",
    "ALE/Boxing-v5",
    "ALE/Breakout-v5",
    "ALE/Carnival-v5",
    "ALE/Casino-v5",
    "ALE/Centipede-v5",
    "ALE/ChopperCommand-v5",
    "ALE/CrazyClimber-v5",
    "ALE/Crossbow-v5",
    "ALE/Darkchambers-v5",
    "ALE/Defender-v5",
    "ALE/DemonAttack-v5",
    "ALE/DonkeyKong-v5",
    "ALE/DoubleDunk-v5",
    "ALE/Earthworld-v5",
    "ALE/ElevatorAction-v5",
    "ALE/Enduro-v5",
    "ALE/Entombed-v5",
    "ALE/Et-v5",
    "ALE/FishingDerby-v5",
    "ALE/FlagCapture-v5",
    "ALE/Freeway-v5",
    "ALE/Frogger-v5",
    "ALE/Frostbite-v5",
    "ALE/Galaxian-v5",
    "ALE/Gopher-v5",
    "ALE/Gravitar-v5",
    "ALE/Hangman-v5",
    "ALE/HauntedHouse-v5",
    "ALE/Hero-v5",
    "ALE/HumanCannonball-v5",
    "ALE/IceHockey-v5",
    "ALE/Jamesbond-v5",
    "ALE/JourneyEscape-v5",
    "ALE/Kaboom-v5",
    "ALE/Kangaroo-v5",
    "ALE/KeystoneKapers-v5",
    "ALE/KingKong-v5",
    "ALE/Klax-v5",
    "ALE/Koolaid-v5",
    "ALE/Krull-v5",
    "ALE/KungFuMaster-v5",
    "ALE/LaserGates-v5",
    "ALE/LostLuggage-v5",
    "ALE/MarioBros-v5",
    "ALE/MiniatureGolf-v5",
    "ALE/MontezumaRevenge-v5",
    "ALE/MrDo-v5",
    "ALE/MsPacman-v5",
    "ALE/NameThisGame-v5",
    "ALE/Othello-v5",
    "ALE/Pacman-v5",
    "ALE/Phoenix-v5",
    "ALE/Pitfall-v5",
    "ALE/Pitfall2-v5",
    "ALE/Pong-v5",
    "ALE/Pooyan-v5",
    "ALE/PrivateEye-v5",
    "ALE/Qbert-v5",
    "ALE/Riverraid-v5",
    "ALE/RoadRunner-v5",
    "ALE/Robotank-v5",
    "ALE/Seaquest-v5",
    "ALE/SirLancelot-v5",
    "ALE/Skiing-v5",
    "ALE/Solaris-v5",
    "ALE/SpaceInvaders-v5",
    "ALE/SpaceWar-v5",
    "ALE/StarGunner-v5",
    "ALE/Superman-v5",
    "ALE/Surround-v5",
    "ALE/Tennis-v5",
    "ALE/Tetris-v5",
    "ALE/TicTacToe3D-v5",
    "ALE/TimePilot-v5",
    "ALE/Trondead-v5",
    "ALE/Turmoil-v5",
    "ALE/Tutankham-v5",
    "ALE/UpNDown-v5",
    "ALE/Venture-v5",
    "ALE/VideoCheckers-v5",
    "ALE/VideoPinball-v5",
    "ALE/Videochess-v5",
    "ALE/Videocube-v5",
    "ALE/WizardOfWor-v5",
    "ALE/WordZapper-v5",
    "ALE/YarsRevenge-v5",
    "ALE/Zaxxon-v5",
]

ATARI57 = [
    "ALE/Alien-v5",
    "ALE/Amidar-v5",
    "ALE/Assault-v5",
    "ALE/Asterix-v5",
    "ALE/Asteroids-v5",
    "ALE/Atlantis-v5",
    "ALE/BankHeist-v5",
    "ALE/BattleZone-v5",
    "ALE/BeamRider-v5",
    "ALE/Berzerk-v5",
    "ALE/Bowling-v5",
    "ALE/Boxing-v5",
    "ALE/Breakout-v5",
    "ALE/Centipede-v5",
    "ALE/ChopperCommand-v5",
    "ALE/CrazyClimber-v5",
    "ALE/Defender-v5",
    "ALE/DemonAttack-v5",
    "ALE/DoubleDunk-v5",
    "ALE/Enduro-v5",
    "ALE/FishingDerby-v5",
    "ALE/Freeway-v5",
    "ALE/Frostbite-v5",
    "ALE/Gopher-v5",
    "ALE/Gravitar-v5",
    "ALE/Hero-v5",
    "ALE/IceHockey-v5",
    "ALE/Jamesbond-v5",
    "ALE/Kangaroo-v5",
    "ALE/Krull-v5",
    "ALE/KungFuMaster-v5",
    "ALE/MontezumaRevenge-v5",
    "ALE/MsPacman-v5",
    "ALE/NameThisGame-v5",
    "ALE/Phoenix-v5",
    "ALE/Pitfall-v5",
    "ALE/Pong-v5",
    "ALE/PrivateEye-v5",
    "ALE/Qbert-v5",
    "ALE/Riverraid-v5",
    "ALE/RoadRunner-v5",
    "ALE/Robotank-v5",
    "ALE/Seaquest-v5",
    "ALE/Skiing-v5",
    "ALE/Solaris-v5",
    "ALE/SpaceInvaders-v5",
    "ALE/StarGunner-v5",
    "ALE/Surround-v5",
    "ALE/Tennis-v5",
    "ALE/TimePilot-v5",
    "ALE/Tutankham-v5",
    "ALE/UpNDown-v5",
    "ALE/Venture-v5",
    "ALE/VideoPinball-v5",
    "ALE/WizardOfWor-v5",
    "ALE/YarsRevenge-v5",
    "ALE/Zaxxon-v5",
]

# Original DQN paper.
ATARI7 = [
    "ALE/BeamRider-v5",
    "ALE/Breakout-v5",
    "ALE/Enduro-v5",
    "ALE/Pong-v5",
    "ALE/Qbert-v5",
    "ALE/Seaquest-v5",
    "ALE/SpaceInvaders-v5",
]

# More or less arbitrary.
ATARI10 = ATARI7 + [
    "ALE/Asteroids-v5",
    "ALE/IceHockey-v5",
    "ALE/MsPacman-v5",
]


def run_assertions():
    assert len(ATARI57) == 57
    assert len(ATARI7) == 7

    import gym

    all_envs = sorted(
        [
            e.id
            for e in gym.envs.registry.all()
            if e.id.startswith("ALE/") and "ram-v5" not in e.id
        ]
    )
    assert ALL_ENVS == all_envs


def main():
    timestamp = time.strftime("%Y%m%d")
    cn = coolname.generate_slug(2)

    run_assertions()

    repeats = 3
    procs = 0

    for env in ATARI10:
        core_name = env[4:-3]
        for n in range(repeats):
            args = [
                "python",
                "sbatch_experiment.py",
                "--project=moolib-atari",
                "--group=%s-%i-%s-%s" % (core_name, n, cn, timestamp),
                # "--dry",
                "env.name=%s" % env,
            ]
            subprocess.run(args)
            procs += 1
    print("Started %i processes" % procs)
    # break


if __name__ == "__main__":
    main()
