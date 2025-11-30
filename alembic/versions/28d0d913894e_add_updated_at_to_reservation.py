from alembic import op
import sqlalchemy as sa

# ✅ très important
revision = "28d0d913894e"
down_revision = "f9c87ca14065"  # c’est bien celui qu’on a vu dans le log
branch_labels = None
depends_on = None

def upgrade():
    #Ajouter la colonne updated_at à la table reservation
    op.add_column(
        "reservations",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.text('CURRENT_TIMESTAMP'),
            onupdate=sa.text('CURRENT_TIMESTAMP')
        )
    )
    # Créer un trigger pour mettre à jour updated_at lors de la modification d'une ligne
    op.execute("""
               CREATE OR REPLACE FUNCTION update_reservation_updated_at()
               RETURNS TRIGGER AS $$
               BEGIN
                   NEW.updated_at = NOW();
                   RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """)
    op.execute("""
               CREATE TRIGGER trg_update_reservation_updated_at
               BEFORE UPDATE ON reservations
               FOR EACH ROW
               EXECUTE FUNCTION update_reservation_updated_at();
               """
)
    
def downgrade():
    # Supprimer le trigger seulement s’il existe
    op.execute(
        "DROP TRIGGER IF EXISTS trigger_update_reservation_updated_at ON reservations;"
    )

    # Supprimer la fonction seulement si elle existe
    op.execute(
        "DROP FUNCTION IF EXISTS update_reservation_updated_at;"
    )

    # Supprimer la colonne seulement si elle existe
    op.execute(
        "ALTER TABLE reservations DROP COLUMN IF EXISTS updated_at;"
    )



