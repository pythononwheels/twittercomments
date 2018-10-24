from twittercomments.models.sql.basemodel import SqlBaseModel


class SqlModel(SqlBaseModel):
    """
        This is the basic class for extensions to put their code
        which is relevant for all models of this type.abs

        Hierarchy: 
         scope:         all         db specific       db specific free
         control:       pow             pow             user/extension
                    modelobject ->    basemodel      ->  sqlmodel
    """