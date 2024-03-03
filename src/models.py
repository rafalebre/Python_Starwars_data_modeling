import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String(100))
    bio = Column(String(350))
    profile_picture = Column(String(500))

    posts = relationship('Post', back_populates='user')
    likes = relationship('Like', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    followers = relationship('Follower', foreign_keys='Follower.user_id', back_populates='user')
    following = relationship('Following', foreign_keys='Following.user_id', back_populates='user')
    stories = relationship('Story', back_populates='user')

class Followers(Base):
    __tablename__ = 'followers'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    follower_id = Column(Integer, ForeignKey('user.id'))
    follow_timestamp = Column(DateTime, nullable=False)

    user = relationship('User', foreign_keys=[user_id], back_populates='followers')
    followers = relationship('User', foreign_keys=[follower_id])

class Following(Base):
    __tablename__ = 'following'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    following_id = Column(Integer, ForeignKey('user.id'))
    follow_timestamp = Column(DateTime, nullable=False)

    user = relationship('User', foreign_keys=[user_id], back_populates='following')
    following = relationship('User', foreign_keys=[following_id])

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    image_url = Column(String(500), nullable=False)
    caption = Column(String(1000))
    creation_timestamp = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='post')
    likes = relationship('Like', back_populates='post')
    comments = relationship('Comment', back_populates='post')

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    like_timestamp = Column(DateTime, nullable=False)


    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    text = Column(String(1000), nullable=False)
    creation_timestamp = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Story(Base):
    __tablename__ = 'story'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    image_url = Column(String(500), nullable=False)
    caption = Column(String(1000))
    creation_timestamp = Column(DateTime, nullable=False)
    expiration_timestamp = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='stories')

class Conversation(Base):
    __tablename__ = 'conversation'
    id = Column(Integer, primary_key=True)

    messages = relationship('Message', back_populates='conversation')

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversation.id'))
    sender_id = Column(Integer, ForeignKey('user.id'))
    receiver_id = Column(Integer, ForeignKey('user.id'))
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    conversation = relationship('Conversation', back_populates='messages')
    sender = relationship('User', foreign_keys=[sender_id])
    
class Hashtag(Base):
    __tablename__ = 'hashtag'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    post_hashtags = relationship('PostHashtag', back_populates='hashtag')

class PostHashtag(Base):
    __tablename__ = 'post_hashtag'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    hashtag_id = Column(Integer, ForeignKey('hashtag.id'))

    post = relationship('Post')
    hashtag = relationship('Hashtag', back_populates='post_hashtags')

class PostInteraction(Base):
    __tablename__ = 'post_interaction'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    interaction_type = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user = relationship('User')
    post = relationship('Post')

class Notification(Base):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    event_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user = relationship('User')

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
