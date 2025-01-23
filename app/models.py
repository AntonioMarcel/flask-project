from datetime import datetime, timezone
from typing import List, Optional

from flask_login import UserMixin
from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, WriteOnlyMapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKeyConstraint
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))

    posts: Mapped[List["Post"]] = relationship(back_populates='author')
    
    roles: Mapped[List["Role"]] = relationship(secondary="user_roles", back_populates="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Role(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    users: Mapped[List["User"]] = relationship(secondary="user_roles", back_populates="roles")

class UserRoles(db.Model):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.id), primary_key=True)

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(140))
    timestamp: Mapped[datetime] = mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)
    
    author: Mapped[User] = relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post {self.body}>"


class OrdenadorDespesas(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    masp: Mapped[str] = mapped_column(String(32), unique=True)
    nome: Mapped[str] = mapped_column(String(255), unique=True)

    dados_nfs: Mapped[List["DadosNfs"]] = relationship(back_populates="ordenador")

class DadosEmpenhos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    uo: Mapped[str] = mapped_column(String(32), index=True)
    ue: Mapped[str] = mapped_column(String(32), index=True)
    ano: Mapped[str] = mapped_column(String(32), index=True)
    empenho: Mapped[str] = mapped_column(String(32), index=True) 
    projeto_atividade: Mapped[str] = mapped_column(String(32)) 
    gmi_fp: Mapped[str] = mapped_column(String(32), index=True)
    elemento_item: Mapped[str] = mapped_column(String(32))
    razao_social_credor: Mapped[str] = mapped_column(String(255), index=True)
    cnpj_cpf_credor: Mapped[str] = mapped_column(String(255), index=True)

    dados_nfs: Mapped[List["DadosNfs"]] = relationship(back_populates="dados_empenho")

    # dados_nfs: Mapped[List["DadosNfs"]] = relationship(
    #     # "DadosNfs",
    #     primaryjoin="and_(DadosNfs.ue==DadosEmpenhos.ue, DadosNfs.ano==DadosEmpenhos.ano, DadosNfs.empenho==DadosEmpenhos.empenho)",
    #     back_populates="dados_empenho",
    #     foreign_keys=("[DadosNfs.ue, DadosNfs.ano, DadosNfs.empenho]")
    # )


class DadosNfs(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    processo_sei: Mapped[str] = mapped_column(String(32), index=True)
    doc_sei_nf: Mapped[str] = mapped_column(String(32), index=True)
    doc_sei_ateste: Mapped[str] = mapped_column(String(32), index=True)
    doc_sei_conformidade: Mapped[str] = mapped_column(String(32), index=True)
    numero_nf: Mapped[str] = mapped_column(String(32), index=True)
    data_emissao: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False) 
    data_entrada: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_vencimento: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_inicio_competencia: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_fim_competencia: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # masp: Mapped[str] = mapped_column(String(32), index=True)
    # nome_ordenador: Mapped[str] = mapped_column(String(255), index=True)
    masp: Mapped[str] = mapped_column(ForeignKey(OrdenadorDespesas.masp), index=True)
    observacoes: Mapped[str] = mapped_column(String(255))
    municipio: Mapped[str] = mapped_column(String(255))
    valor_nf: Mapped[float] = mapped_column(Float)
    ue: Mapped[str] = mapped_column(String(32), index=True)
    ano: Mapped[str] = mapped_column(String(32), index=True)
    empenho: Mapped[str] = mapped_column(String(32), index=True)

    __table_args__ = (
        ForeignKeyConstraint(['ue', 'ano', 'empenho'],
                             [DadosEmpenhos.ue, DadosEmpenhos.ano, DadosEmpenhos.empenho], "dados_empenho_fk"),
    )

    # gmi_fp: Mapped[str] = mapped_column(String(32), index=True)
    # nome_credor: Mapped[str] = mapped_column(String(255), index=True)
    # cnpj_cpf_credor: Mapped[str] = mapped_column(String(32), index=True)
    conformidade: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    banco: Mapped[str] = mapped_column(String(32), index=True)
    agencia: Mapped[str] = mapped_column(String(32), index=True)
    conta: Mapped[str] = mapped_column(String(32), index=True)

    ordenador: Mapped["OrdenadorDespesas"] = relationship(back_populates="dados_nfs")
    dados_empenho: Mapped["DadosEmpenhos"] = relationship(back_populates="dados_nfs")

    @property
    def formatted_valor_nf(self):
            return f"R$ {self.valor_nf:,.2f}".replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")

    # dados_empenho: Mapped["DadosEmpenhos"] = relationship(
    #     back_populates="dados_nfs",
    #     primaryjoin="and_(DadosNfs.ue==DadosEmpenhos.ue, DadosNfs.ano==DadosEmpenhos.ano, DadosNfs.empenho==DadosEmpenhos.empenho)",
    #     foreign_keys=("[DadosEmpenhos.ue, DadosEmpenhos.ano, DadosEmpenhos.empenho]"),
    # )

    # dados_empenho = relationship(
    #     "DadosEmpenhos",
    #     primaryjoin="and_(DadosNfs.ue==DadosEmpenhos.ue, DadosNfs.ano==DadosEmpenhos.ano, DadosNfs.empenho==DadosEmpenhos.empenho)",
    #     foreign_keys=("[DadosEmpenhos.ue, DadosEmpenhos.ano, DadosEmpenhos.empenho]")
    # )

    # dados_empenho_id: Mapped[int] = mapped_column(ForeignKey(DadosEmpenhos.id), index=True)
    # dados_empenho: Mapped["DadosEmpenhos"] = relationship(back_populates="dados_nfs")

    # ue: Mapped[str] = mapped_column(ForeignKey(DadosEmpenhos.ue), index=True)
    # ano: Mapped[str] = mapped_column(ForeignKey(DadosEmpenhos.ano), index=True)
    # empenho: Mapped[str] = mapped_column(ForeignKey(DadosEmpenhos.empenho), index=True)

    # __table_args__ = (
    #     ForeignKeyConstraint(['ue', 'ano', 'empenho'],
    #                          [DadosEmpenhos.ue, DadosEmpenhos.ano, DadosEmpenhos.empenho]),
    # )

    # dados_empenho: Mapped["DadosEmpenhos"] = relationship(back_populates="dados_nfs")

    # dados_empenho_id: Mapped[int] = mapped_column(ForeignKey(DadosEmpenhos.id), index=True)
    # dados_empenho: Mapped[DadosEmpenhos] = relationship(
    #     primaryjoin="and_(foreign(DadosNfs.ue) == DadosEmpenhos.ue, "
    #     "foreign(DadosNfs.ano) == DadosEmpenhos.ano, "
    #     "foreign(DadosNfs.empenho) == DadosEmpenhos.empenho)"
    # )


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
