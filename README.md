# Nordale Color Matcher Utility

A community-driven utility designed to help builders match real-world color palettes to the specific blocks available in the Nordale modpack.

## Purpose
This tool allows you to input a color or upload an image to find the closest block match based on texture color data. It helps streamline the building process by quickly identifying blocks that fit your aesthetic vision.

## Disclaimer
This is a community-created utility. It is **not** an official product of the mod authors listed below. This tool does not distribute, modify, or contain any copyrighted art assets or textures. It only uses publicly available metadata (names, mod sources, and hex codes) to provide a search index for your local installation of these mods.

## Credits & Mod Acknowledgments
This utility indexes metadata from the following mods. All textures and creative works remain the property of their respective creators:

ArtemisLib, AutoRegLib, BetterFps, BiblioCraft, BiomesOPlenty, CTM, ChickenChunks, Chisel, CodeChickenLib, CreativeCore, Currency, CustomPlayerModels, DynamicSurroundings, FTBLib, FTBUtilities, FancyFluidStorage, ForgeMultipart, FutureVersions, Gulliver Reborn, ImmersiveEngineering, ImmersivePosts, ImmersiveRailroading, IndustrialRenewal, IndustrialWires, LagGoggles, LittleFrames, LittleTiles, MCT, MrTJPCore, NordaleEconomyMod, OpenComputers, OptiFine, OreLib, Pam's HarvestCraft, ProjectRed, Quark, QuarkOddities, ReAuth, RedstoneFlux, Tails, TickCentral, TrackAPI, Trackside_Decor, UniversalModCore, WirelessRedstone, akidecor, autocrafter, blockcraftery, censoredasm, cfm (MrCrayfish's Furniture Mod), cmm_nordale, effortlessbuilding, engineersdecor, flatcoloredblocks, immersivepetroleum, jei, journeymap, mcjtylib, mixinbooter, mysticallib, nordalesignals, performant, railstuff, rsgauges, theoneprobe, time-and-wind, vintagefix, worldedit, xnet

*If you are the author of one of these mods and would like to be credited differently or have concerns about this utility, please reach out.*

## How to use
1. Ensure the modpack is installed locally on your system.
2. Run the `app_web.py` script using the Streamlit runner.
3. Use the provided interface to pick colors or upload your reference images.

## Setup Requirements
* Python 3.x
* Required libraries: `streamlit`, `Pillow`, `streamlit-image-coordinates`, `streamlit-paste-button`
