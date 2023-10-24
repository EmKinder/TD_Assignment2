
#Asset Publishing System Pseudocode - Emily Kinder 14160170

def Window(): 
    #Window 1: Button click set piece -> IsSetPiece()
    #Window 2: Button click set -> IsSet()
    #Window 3: Button click layout -> IsCamera()
    #Window 4: Button click save file -> SaveFile()
    #Window 5: Button click publish file -> PublishFile()

def IsSetPiece():
    #IsSetPiece 1: Remove previous asset instances
    #IsSetPiece 2: Get selected asset from scene
    #IsSetPiece 3: Get asset transform 
    #IsSetPiece 4: Get asset mesh 
    #IsSetPiece 5: Get asset keyframes 
    #IsSetPiece 6: Get asset nodes
    #IsSetPiece 7: Create asset instance with above parameters
    #IsSetPiece 8: FolderType = SetPieces

def IsSet():
    #IsSet 1: Remove previous asset instances
    #IsSet 2: Get list of all selected assets from scene
    #IsSet 3: Loop through list of assets 
        #IsSet Loop 1: ThisAsset = IsSetPiece()
        #IsSet Loop 2: Add ThisAsset instance to new list 
    #IsSetPiece 4: FolderType = Sets

def IsCamera(): 
    #GetCamera 1: Remove previous asset instances
    #GetCamera 2: Get seleced camera from scene 
    #GetCamera 3: Get camera transform 
    #GetCamera 4: Get camera keyframes
    #GetCamera 5: Get camera aperture 
    #GetCamera 6: Get camera focal length
    #GetCamera 7: Create asset instance with above parameters
    #GetCamera 8: FolderType = Cameras


def SaveFile():
    #Save 1: Get WIP\\FolderType directory 
    #Save 2: Check if directory for this asset exists
        #Save IF 1: true -> filePath = existingDirectory 
        #Save IF 2: false -> filePath = WIP\\FolderType\\AssetName
    #Save 3: Check if current version exists 
        #Save IF 1: true -> versionNumber++ 
        #Save IF 2: false -> break
    #Save 4: Save file to filePath\\AssetName+VersionNumber as MayaAscii


def PublishFile():
    #Publish 1: Loop through asset list if set, else just perform once
        #Publish Loop 1: Run integrity check with asset instance - (Keegan's section)
        #Publish Loop 1: If integrity check successful 
            #1: Updated file name 
            #2: Asset = IntegrityCheckedAsset
    #Publish 2: Access WIP folder through OGassetName
    #Publish 3: Loop through WIP files to access most recent version 
    #Publish 4: thisAssetNumber = most recent WIP number + 1
    #Publish 5: Find source directory
    #Publish 6: Find Alembic directory in source
    #Publish 7: Find FBX directory in source 
    #Publish 8: Create file path -> source directory + thisAsset
    #Publish 9: Create Alembic file path
    #Publish 10: Create FBX file path 
    #Publish 11: Save file as MayaAscii 
    #Publish 12: If set -> Loop through list and combine into one condensed asset
    #Publish 13: Save file path as Alembic 
    #Publish 14: Save file path as FBX