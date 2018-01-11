Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  resource :dashboard, only: [:show], controller: 'dashboard', url: nil
  resource :settings
  root 'home#index'
end
