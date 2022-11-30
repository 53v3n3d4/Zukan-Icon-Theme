class ArticlesController < ApplicationController
  def index
    @articles = Article.recent
  end

  def show
    @article = Article.find(params[:id])
    fresh_when etag: @article
  end

  def create
    article = Article.create!(article_params)
    redirect_to article
  end

  private
    def article_params
      params.require(:article).permit(:title, :content)
    end
end

class Article < ApplicationRecord
  belongs_to :author, default: -> { Current.user }
  has_many   :comments

  has_one_attached :cover_image
  has_rich_text :content, encrypted: true
  enum status: %i[ drafted published ]

  scope :recent, -> { order(created_at: :desc).limit(25) }

  after_save_commit :deliver_later, if: :published?

  def byline
    "Written by #{author.name} on #{created_at.to_s(:short)}"
  end

  def deliver_later
    Article::DeliveryJob.perform_later(self)
  end
end

Rails.application.routes.draw do
  resources :articles do    # /articles, /articles/1
    resources :comments     # /articles/1/comments, /comments/1
  end

  root to: "articles#index" # /
end